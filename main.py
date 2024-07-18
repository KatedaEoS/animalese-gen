from pydub import AudioSegment
from voicehelper import VoiceHelper
from slicer import KanaSlicer, PinYinSlicer
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Animalese Voice Generator")
    parser.add_argument("rootdir", type=str)
    parser.add_argument("gender", type=str)
    parser.add_argument("tone", type=str)
    parser.add_argument("language", type=str, choices=["zh", "ja"])
    parser.add_argument("text", type=str)
    parser.add_argument("-o", "--output", type=str, default="result.mp3")
    parser.add_argument("--cutin", type=int, default=1000)
    parser.add_argument("--cutout", type=int, default=12000)
    parser.add_argument("--space", type=int, default=300)

    args = parser.parse_args()

    bank = VoiceHelper(args.rootdir, args.gender, args.tone)
    bank.kana["fu"] = bank.kana["hu"]
    bank.kana["shi"] = bank.kana["si"]

    sound = AudioSegment.silent(duration=300)
    res = []

    if args.language == "zh":
        pinyin = PinYinSlicer(bank.kana.keys())
        res = pinyin.pinyin_slice(args.text)
    elif args.language == "ja":
        kana = KanaSlicer(bank.kana.keys())
        res = kana.kana_slice(args.text)
    else:
        raise ("Error: unrecognized language")

    last_syll = ""

    for count, syll in res:
        s = None
        if syll == "":
            s = AudioSegment.silent(duration=args.space)
        elif count >= 3:
            print(f"Rendering {count}x {syll}")
            s = bank.find_loop(syll)
        else:
            print(f"Rendering {last_syll}, {syll}")
            s = bank.find(last_syll + syll)
            last_syll = syll[-1]

        if s is not None:
            if syll != "":
                raw = s.raw_data[args.cutin : -args.cutout]
                s = s._spawn(raw)
                for _ in range(1 if count < 3 else count):
                    sound = (
                        sound
                        + s.fade_in(5).fade_out(5)
                        + AudioSegment.silent(duration=5)
                    )
            else:
                for _ in range(1 if count < 3 else count):
                    sound = sound + s

    sound.export(args.output, format="mp3")
