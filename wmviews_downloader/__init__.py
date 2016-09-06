# coding: utf-8
import requests
import os
from datetime import date, datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

endpoint = 'https://dumps.wikimedia.org/other/pageviews/{0:%Y}/{0:%Y-%m}/'
filenames = dict(
    pageviews='pageviews-{0:%Y%m%d}-{0:%H}0000.gz',
    projectviews='projectviews-{0:%Y%m%d}-{0:%H}0000',
)


def parse_date(date_str):
    return datetime.strptime(date_str, '%Y%m')


class DLClient(object):
    def __init__(self, outdir='./', parallelism=3):
        self.outdir = outdir
        self.parallelism = parallelism

    def generate_urls(self, month, mode):
        tgt_month = month.month
        cur_date = month
        baseurl = endpoint.format(month)
        files = []
        while cur_date.month == tgt_month:
            files.append(filenames[mode].format(cur_date))
            cur_date += timedelta(hours=1)
        return baseurl, files

    def pageviews(self, month):
        if type(month) is not date:
            month = parse_date(month)
        baseurl, files = self.generate_urls(month, 'pageviews')
        """
        for fname in baseurl:
            print fname
            url = baseurl + fname
            content = requests.get(url).content
            fpath = os.path.join(self.outdir, fname)
            with open(fpath, 'w') as fp:
                fp.write(content)
        """
        for result in as_completed(self.get_concurrent(baseurl, files)):
            fname, content = result.result()
            print(fname)
            fpath = os.path.join(self.outdir, fname)
            with open(fpath, 'w') as fp:
                fp.write(content)

    def projectviews(self):
        pass

    def download(self, url, fname):
        f = requests.get(url)
        return fname, f.content

    def get_concurrent(self, baseurl, files):
        with ThreadPoolExecutor(self.parallelism) as executor:
            result = [executor.submit(self.download, baseurl+fname, fname)
                       for fname in files]
        return result
