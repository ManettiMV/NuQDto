# FBOT PNG Generator

This repository contains a PNG image generator with custom text and an integrated phoenix symbol, designed for the fast production of visually distinctive artwork.

The project was developed to simplify the creation of customized lettering by using a font from the `vox` folder and a phoenix illustration that can be adjusted according to the team's needs.

## Overview

The main script is [NuQDto.py](NuQDto.py), and it uses Python + Tkinter + Pillow to:

- receive user input text;
- choose a font from the `vox` folder;
- place the phoenix image as a visual element on the side;
- generate a PNG in `results` with a configurable layout.

The interface allows changing parameters such as:

- font size;
- fixed phoenix height;
- vertical scale;
- symbol width;
- spacing between elements;
- page margin.

## Custom phoenix

An important part of the project is the ability to replace or adapt the phoenix image.

The project includes a custom creator for the phoenix visual identity, allowing the artwork to be easily modified to maintain the desired brand style. In other words, the phoenix image is not just a static asset: it can be adjusted, refreshed, or replaced depending on project needs.

This makes the generator more flexible for campaigns, visual materials, personal branding, or any specific use by the team.

## Built specifically for the FBOT team

This project was created specifically for the FBOT team, focused on meeting internal visual generation and automated art production needs with a personalized style.

The structure and settings of the generator were designed to make the production of images with a consistent visual identity easier without depending on complex external tools.

## Repository structure

- [NuQDto.py](NuQDto.py): main generator script.
- [vox](vox): folder containing the fonts used in the project.
- [results](results): output folder for generated PNG images.
- [examples](examples): space for examples or auxiliary materials.

## How to use

1. Place the desired font inside the `vox` folder.
2. Make sure the phoenix image is present in the project root as `fenix.png`.
3. Run [NuQDto.py](NuQDto.py).
4. Enter the desired text.
5. Adjust the size and parameters in the settings panel if needed.
6. Generate the image and save the result in `results`.

## Requirements

- Python 3
- Tkinter
- Pillow

Install the main dependency with:

```bash
pip install pillow
```

## Team reference

The FBOT team is on GitHub:

https://github.com/FBOTWork

## Summary

This project combines text editing, custom drawing, and a strong visual identity based on the team logo, with a focus on fast and flexible production for the FBOT team. The ability to change the phoenix image using a custom creator makes the repository especially useful for continuous visual adaptation and personalized artwork.
