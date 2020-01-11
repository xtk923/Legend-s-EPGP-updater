#-*-coding=utf-8-*-
import sys
import pandas as pd

guild_rank = {
    "会长" : 1,
    "书记" : 2, 
    "官员" : 3, 
    "队长": 4,
    "一团": 5,
    "二团": 6,
    "三团": 7,
    "会员": 8,
    "见习": 9
}



def main():
    filename = sys.argv[1]
    file = open(filename, "r")
    raw = file.readline()
    file.close()

    # This JSON file is not properly formated.
    # We crop its middle part as the pure content.
    trail = ",\"timestamp\""
    content = raw.split(":")[1][0:-len(trail)]


    cols = ['角色', '职业', '会阶', 'EP', 'GP', "PR"]
    df = pd.read_json(content, encoding="gb2312")
    df.columns = cols

    # remove those with zero EP
    for exclude in ["会员", "见习", "三团", "小黑屋"]:
        df = df[df['会阶'] != exclude ]

    # sort by rank and class
    df['guild rank'] = df['会阶'].map(guild_rank)
    df = df.sort_values(by=['guild rank', '职业'])
    del df['guild rank']

    for col in ["EP", "GP", "PR"]:
        df[col] = list(map(lambda x :
                           "{:.2f}".format(x), df[col]))

    tableLine = pd.DataFrame(
        [['---' for x in range(len(df.columns.values))]],
        columns = df.columns.values)

    df = pd.concat([tableLine, df])

    print(df.head())
    df.to_csv('./result.md', encoding='utf-8', index=False, sep="|")

if __name__ == "__main__":
    main()
