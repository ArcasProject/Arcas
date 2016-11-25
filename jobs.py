import os
import tqdm
years = list(range(1990, 2011))
title = ["Prisoner Dilemma", "Iterated Prisoner Dilemma"]
apis = ['ieee', 'arxiv']
records = [i * 100 for i in range(1, 10)]
pbar = tqdm.tqdm(total=(len(years)*len(title)*len(apis)*len(records)))


for yr in years:
    for ti in title:
        for ap in apis:
            for st in records:
                os.system("python scrape.py -p {} -t '{}' -y {} -r 100 -s {}".format(ap, ti, yr, st))

        pbar.update()
pbar.close()
