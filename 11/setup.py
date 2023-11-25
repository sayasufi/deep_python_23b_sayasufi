from setuptools import setup, Extension


def main():
    setup(name="cjson",
          version="1.0.1",
<<<<<<< HEAD
          author="Ryabov Semyon",
=======
          author="Stas Belosludcev",
>>>>>>> origin/main
          ext_modules=[Extension('cjson', ['./cjson.c'])]
          )


if __name__ == "__main__":
    main()