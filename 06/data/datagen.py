from argparse import ArgumentParser
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor


def generate_url(url):
    page = urlopen("https://en.wikipedia.org/wiki/Special:Random")
    return page.url


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", help="Filename")
    parser.add_argument("-k", default=1, help="URLs count")

    args = parser.parse_args()

    with open(args.f, "w") as file:
        with ThreadPoolExecutor() as executor:
            urls = executor.map(generate_url, range(int(args.k)))

            for url in urls:
                file.write(url + "\n")
