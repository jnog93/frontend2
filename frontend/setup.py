from setuptools import find_packages, setup

setup(
    name="home-assistant-frontend",
    version="20210804.1",
    description="The Home Assistant frontend compiled for raceland homeassistant fork",
    url="https://github.com/RACELAND-Automacao-Lda/frontend",
    author="Raceland",
    author_email="andre.teixeira@raceland.pt",
    license="Apache-2.0",
    packages=find_packages(include=["hass_frontend", "hass_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)
