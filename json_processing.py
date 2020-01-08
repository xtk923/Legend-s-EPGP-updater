#-*-coding=utf-8-*-
import sys
import pandas as pd

def main():
    filename = sys.argv[1]
    file = open(filename)
    raw = file.readline()
    file.close()

    # This JSON file is not properly formated.
    # We crop its middle part as the pure content.
    trail = ",\"timestamp\""
    content = raw.split(":")[1][0:-len(trail)]


    cols = ['Character', 'Class', 'Rank', 'EP', 'GP', "PR"]
    df = pd.read_json(content, encoding="gb2312")
    df.columns = cols

    # remove those with zero EP
    df = df[df['EP'] != 0]

    # sort by rank and class
    df = df.sort_values(by=['Rank', 'Class'])
    tableLine = pd.DataFrame([['---' for x in range(len(df.columns.values))]],
                            columns = df.columns.values)

    df = pd.concat([tableLine, df])
    print(df.head())
    df.to_csv('./result.md', encoding='utf-8', index=False, sep="|")

if __name__ == "__main__":
    main()
