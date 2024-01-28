import imp
from importlib.resources import path
import pathlib
from setuptools import setup, find_packages


class Module:
    base_dir = pathlib.Path(__file__).parent.absolute()
    module_dir = "controller"

    @property
    def version(self):
        with open(self.base_dir / "version") as file:
            return file.readline().strip()

    @property
    def long_desc(self):
        with open(self.base_dir / "readme.md") as file:
            return file.read().strip()

    @property
    def packages(self):
        with open(self.base_dir / "requirements.txt") as file:
            return [package.strip() for package in file.readlines() if package]

    @property
    def license(self):
        with open(self.base_dir / "license") as file:
            return file.read().strip()

    def add_version(self):
        version_line = '__version__ = "{}"\n'.format(self.version)
        init_file_path = self.base_dir / self.module_dir / "__init__.py"
        try:
            with open(init_file_path) as init_file:
                code = init_file.readlines()
        except FileNotFoundError:
            code = [version_line]
        else:
            import_position = None
            for index, line in enumerate(code):
                if "__version__" in line:
                    code[index] = version_line
                    break
                if "import" in line:
                    import_position = index
            else:
                if import_position is not None:
                    new_line_pos = import_position + 1
                    code.insert(new_line_pos, version_line)
                    code.insert(new_line_pos, "\n\n")
                else:
                    code.insert(0, "\n\n")
                    code.insert(0, version_line)
        with open(init_file_path, "w") as init_file:
            init_file.writelines(code)
        return self

    def install(
        self, author: str, email: str, url: str = "", name: str = None, desc: str = None
    ):
        setup(
            name=name or self.module_dir,
            version=self.version,
            author=author,
            author_email=email,
            url=url,
            license=self.license,
            packages=find_packages(".", include=[self.module_dir]),
            package_dir={"": "."},
            include_package_data=True,
            description=desc or "",
            long_description=self.long_desc,
            long_description_content_type="text/markdown",
            install_requires=self.packages,
            python_require=">=3.8",
            zip_safe=True,
            classifiers=[
                "Development Status :: 3 - Alpha"
                if "dev" in self.version
                else "Development Status :: 4 Beta"
                if "rc" in self.version
                else "Development Status :: 5 Production/Stable"
            ],
        )


Module().add_version().install(
    "Dmitriy Amelchenko",
    "d.a.xolloo@gmail.com",
    url="https://gitlab.com/xolloo/aiohttp_controller",
    desc="Url controller.",
)