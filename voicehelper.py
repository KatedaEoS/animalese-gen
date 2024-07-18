from pydub import AudioSegment
import os, re


class VoiceHelper:
    def __init__(self) -> None:
        self.gender = None
        self.tone = None
        self.kana = None
        self.kana_ex = None
        self.loop = None

    def __init__(self, rootdir: str, gender: str, tone: str) -> None:
        self.kana = None
        self.kana_ex = None
        self.loop = None
        self.read(rootdir, gender, tone)

    def read(self, rootdir: str, gender: str, tone: str) -> None:
        self.gender = gender
        self.tone = tone
        self.kana = {}
        self.kana_ex = {}
        self.loop = {}
        voice_dir = os.path.join(rootdir, gender, tone)
        file_list = os.listdir(voice_dir)
        for f in file_list:
            file_path = os.path.join(voice_dir, f)
            if not os.path.isfile(file_path):
                continue
            name = re.findall("[a-zA-Z]+", f)
            if len(name) < 5 or name[4] != "wav":
                continue
            voice = AudioSegment.from_wav(file_path)
            voice_type = name[2]
            voice_syll = name[3]

            if voice_type == "Kana":
                self.kana[voice_syll] = voice
            elif voice_type == "KanaEx":
                leading = voice_syll[0:1]  # aeiou
                syll = voice_syll[1:]
                if leading not in self.kana_ex:
                    self.kana_ex[leading] = {}
                self.kana_ex[leading][syll] = voice
            elif voice_type == "Loop":
                self.loop[voice_syll] = voice
            else:
                print(f"Warning: unhandled file: {f}")

    def find(self, diphtho: str) -> AudioSegment:
        leading = diphtho[0:1]
        syll = diphtho[1:]
        # print(f"finding {diphtho}")
        if leading in self.kana_ex:
            if syll in self.kana_ex[leading]:
                # print(f"found ex {leading}{syll}")
                return self.kana_ex[leading][syll]
        if diphtho in self.kana:
            # print(f"found diphtho {diphtho}")
            return self.kana[diphtho]
        if syll in self.kana:
            # print(f"found syll {syll}")
            return self.kana[syll]
        print(f"Warning: cannot satisfy voice: {diphtho}")
        return None

    def find_loop(self, syll: str) -> AudioSegment:
        if syll in self.loop:
            return self.loop[syll]
        else:
            print(f"Warning: cannot satisfy loop voice: {syll}")
            return self.find(syll)
