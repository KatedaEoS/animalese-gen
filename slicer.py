import re


class Slicer:
    def __init__(self) -> None:
        pass

    def fold(self, result: list[str]) -> list[list]:
        final_result = []
        for i in result:
            if (
                len(final_result) > 0
                and i in {"a", "e", "i", "o", "u"}
                and final_result[-1][1] == i
            ):
                final_result[-1][0] += 1
            else:
                final_result.append([1, i])

        while len(final_result) > 0 and final_result[-1][1] == "":
            final_result.pop()

        return final_result


class KanaSlicer(Slicer):
    def __init__(self) -> None:
        self.sylls = set()

    def __init__(self, sylls: set) -> None:
        self.init_set(sylls)

    def init_set(self, sylls: set) -> None:
        self.sylls = set(sylls)

    def kana_slice(self, input: str, sokuon: bool = True) -> list[list]:
        now = ""
        tsustop = 0
        result = []
        input = input.lower() + "   "
        for c in input:
            if not str.isalpha(c):
                for i in now:
                    if i in self.sylls:
                        result.append(i)
                now = ""
                result.append("")
                tsustop = 0
                continue

            now = now + c
            if (
                sokuon
                and len(now) >= 3
                and now[0] not in {"a", "e", "i", "o", "u", "n"}
                and now[0] == now[1]
            ):
                now = now[1:]
                tsustop += 1
            if (len(now) >= 2 and now in self.sylls) or (
                len(now) >= 3 and now[1:] in self.sylls
            ):
                for _ in range(tsustop):
                    result.append("")
                if now not in self.sylls:
                    if now[0:1] in self.sylls:
                        result.append(now[0:1])
                    now = now[1:]
                tsustop = 0
                result.append(now)
                now = ""
            elif len(now) >= 3 and now[0:1] in self.sylls:
                result.append(now[0:1])
                now = now[1:]

            if len(now) >= 4:
                now = now[1:]

        return self.fold(result)


class PinYinSlicer(KanaSlicer):
    def pinyin_slice(self, input: str) -> list[list]:
        input = re.sub(r"[^\w\s]", " , ", input)
        input = re.sub(r"[!\"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]", " , ", input)

        input = input.replace("l", "r")
        input = input.replace("ng", "n")
        input = input.replace("ca", "cha")
        input = input.replace("ce", "che")
        input = input.replace("ci", "chi")
        input = input.replace("cu", "chu")
        input = input.replace("co", "cho")

        input = input.replace("zh", "z")
        input = input.replace("q", "ch")
        input = input.replace("x", "s")
        input = input.replace("sh", "s")

        input = input.replace("jiu", "jo")
        input = input.replace("jia", "ja")
        input = input.replace("ji", "je")

        input = input.replace("uo", "o")

        input = input.replace("yi", "i")
        input = input.replace("wu", "u")

        print(input)

        token_list = re.findall("[a-zA-Z,]+", input)
        result = ""
        for i in token_list:
            if i == ",":
                result += " "
            else:
                result += i

        return self.kana_slice(result, False)
