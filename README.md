<a href="https://www.buymeacoffee.com/pierpaolo" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a> <br>

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

  <h3 align="center">Epidemics Modelling</h3>

## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgments](#acknowledgments)

## About The Project

Interactive Epidemics Modelling dashboard created using Streamlit and deployed on an Amazon Web Services (AWS) EC2 Linux Instance. In this dashboard, has been used COVID-19 as example case study (in order to provide a practical demonstration) but by changing the modelling parameters (eg. SIR model), parts of this dashboard toolkit can be used also to model many other types of epidemics in general.

![](dist/epid.jpg)

This dashboard is currently available live at [this link](http://3.22.240.181:8501) (the dashboard might not be anymore publicly available online after May 2020).

## Getting Started

This dashboard was created using `Python 3.6`. To run the code locally, start by installing PyTorch as per the [docs](https://pytorch.org/get-started/locally/) (PyTorch installation is just required if you want to run all the Jupyter Notebooks, not the web application). Then run in terminal the commands below:

```bash
# Clone the repository.
git clone https://github.com/pierpaolo28/Epidemics-Modelling.git
cd Epidemics-Modelling

# (Windows Optional) Create a new Python environment and activate it.
python -m venv .env
.env\Scripts\activate

# (Ubuntu Optional) Create a new Python environment and activate it.
python3 -m venv .env
source .env/bin/activate

# Install the dependencies.
pip install -r requirements.txt

# Run dashboard in localhost (a web-broswer page is automatically going to be opened)
streamlit run src/main.py
```

## Docker Support

In case you want to use this application in a Docker container, just follow the next few steps:

```bash
# Clone the repository.
git clone https://github.com/pierpaolo28/Epidemics-Modelling.git
cd Epidemics-Modelling

# Build the container
docker build -f Dockerfile -t app:latest .

# Run the container
docker run --name Epid_App -p 8501:8501 app:latest
```

At this point, the web application should be up and running at the following URL in your browser: [http://localhost:8501/](http://localhost:8501/).

## Contributing

In case you want to contribute to this open source project, please use the following instructions:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License.

## Contact

Your Name - [@Pier_Paolo_28](https://twitter.com/Pier_Paolo_28) - [LinkedIn](https://www.linkedin.com/in/pierpaolo28/)

Project Link: [https://github.com/pierpaolo28/Epidemics-Modelling](https://github.com/pierpaolo28/Epidemics-Modelling)

## Acknowledgments

[1] Pearl, Judea, and Dana Mackenzie. *The book of why: the new science of cause and effect*. Basic Books, 2018.

[2] Olsen, Jørn, et al. *An introduction to epidemiology for health professionals*. 2010.

[contributors-shield]: https://img.shields.io/github/contributors/pierpaolo28/Epidemics-Modelling.svg?style=flat-square
[contributors-url]: https://github.com/pierpaolo28/Epidemics-Modelling/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/pierpaolo28/Epidemics-Modelling.svg?style=flat-square
[forks-url]: https://github.com/pierpaolo28/Epidemics-Modelling/network/members
[stars-shield]: https://img.shields.io/github/stars/pierpaolo28/Epidemics-Modelling.svg?style=flat-square
[stars-url]: https://github.com/pierpaolo28/Epidemics-Modelling/stargazers
[issues-shield]: https://img.shields.io/github/issues/pierpaolo28/Epidemics-Modelling.svg?style=flat-square
[issues-url]: https://github.com/pierpaolo28/Epidemics-Modelling/issues
[license-shield]: https://img.shields.io/github/license/pierpaolo28/Epidemics-Modelling.svg?style=flat-square
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/pierpaolo28/
