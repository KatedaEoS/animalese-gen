import pypinyin, argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simple Chinese to Pinyin")
    parser.add_argument("text", type=str)

    args = parser.parse_args()

    pinyin_list = pypinyin.lazy_pinyin(args.text)
    result = ""
    for i in pinyin_list:
        result += i + " "
    result.strip()

    print(f'"{result}"')
