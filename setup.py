from setuptools import find_packages, setup


def read_requirements(filename: str):
    with open(filename) as requirements_file:
        requirements = []
        for line in requirements_file:
            line = line.strip()
            if line.startswith("#") or len(line) <= 0:
                continue
            requirements.append(line)
    return requirements


setup(
    name="ros2_numpy",
    version="0.0.5",
    description="Convert ROS2 messages to and from numpy arrays",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="",
    url="https://github.com/nitesh-subedi/ros2_numpy",
    author="Tom",
    author_email="tom@boxrobotics.ai",
    maintainer="Nitesh Subedi",
    maintainer_email="074bme624.nitesh@pcampus.edu.np",
    license="MIT",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    install_requires=read_requirements("requirements.txt"),
    python_requires=">=3.10",
)
