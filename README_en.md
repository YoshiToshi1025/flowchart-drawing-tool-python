以下は、README用文章の英訳です（Markdown構造を維持しています）。

---

# flowchart-drawing-tool-python

Simple Flowchart Drawing Tool (Python Version)

## Overview

This project provides a **Simple Flowchart Drawing Tool (Python version)** that allows you to easily create flowcharts.

## Project Purpose

* Have you ever experienced the following frustrations when creating flowcharts?

  * During requirement definition to detailed design, you want to use simple flowcharts to consider business flows or processing logic, but you can’t find a tool that is easy to draw with and practical for business use, which makes you frustrated every time you need to create a flowchart.
  * You create flowcharts in Excel or PowerPoint, but it takes a long time to adjust them into a satisfactory shape, and repeated editing becomes tiresome.
  * In the age of generative AI, don’t text-heavy specification documents feel outdated? Even when you ask generative AI to create flowcharts, the results are often unsatisfactory and difficult to edit.

* With these issues in mind, this tool was developed in Python with the goal of being a **casually usable flowchart drawing tool**.

* Since the basic features required for drawing simple flowcharts have been mostly implemented, a provisional version is now released.

* Note: This source code was created using ChatGPT and then manually modified, so some parts of the code are not yet well organized. It will be gradually refactored (sorry!).

* **New Feature**: Integration with generative AI (GPT-5.2) to support automatic flowchart generation.
  (Each flowchart element and its connections still need to be adjusted manually.)

<img width="100%" src="example/output_example.png" />

## Installation

* Prerequisites

  * An environment where Python code can be executed and where the Tkinter Canvas library is available.
    (It does not work in web-based environments such as Google Colaboratory. On macOS, Tkinter must be properly configured.)

* Installation Steps

  1. Check out this project’s code into a Python-executable environment.

  2. In the checkout folder, run `pip install -r requirements.txt` to install the required packages.

  3. If you want to automatically generate process flows using generative AI, create a `.env` file in the checkout folder and describe your OpenAI API Key in the following format:
     (For details on how to obtain an OpenAI API Key, see `Docs/OpenAI_API_Keyの取得方法(ChatGPT生成).md`.)

     **“.env file content (single line)”**
     `OPENAI_API_KEY=(API Key obtained from OpenAI)`

  4. Run `flowchart_tool.py` to launch the flowchart drawing tool.

## Usage

* **Placement**: Select Process, Decision, Terminator, or I/O from the menu, then click on the canvas to place an element.

  * **Drawable Elements**

    * Terminator: Start, End, Subroutine
    * Process: Processing
    * Decision: Branch
    * I/O: Input / Output
* **Connection**: Select Link from the menu, then select the source element and the destination element in order to draw a connecting line.
* **Text Editing**: Double-click an element or a link on the canvas to enter text edit mode.
* **Move**: Select Select from the menu and drag & drop elements on the canvas to move them.
* **Element Selection**: Select Select from the menu and click an element to select it.
* **Multiple Selection**: Select Select from the menu and drag a rectangular area from an empty space to select multiple elements within the rectangle.
* **Delete**: Click the Delete button in the menu to delete the selected element(s) and their links.
* **UNDO / REDO**: Use the UNDO and REDO buttons in the menu to undo or redo the most recent edit operations.
* **Import / Export**: Export the canvas content as an image (JPEG/PNG) or JSON file, or import a saved JSON file to redraw the flowchart.
* **Grid**: Turn on the Grid checkbox in the menu to display a grid and constrain element placement to the grid.
* **Automatic Flow Generation**: Turn on the AI-generation checkbox in the menu, specify the process flow to be automatically generated in the right-side panel, and click the Generate button to create a flowchart automatically.
  (Please manually adjust the layout of the generated flow.)
* **Manual Link Routing Adjustment**: When a link is selected, use `CTRL + Mouse Wheel` to cycle connection points, and `SHIFT + Mouse Wheel` to adjust the routing offset distance.

*Sample JSON files are provided in the `example` folder. These files can be loaded using [Load JSON].*

## Operation

* The current provisional version is intended to be used as follows:

  1. Launch the flowchart drawing tool.
  2. For manual creation:

     1. For new creation, draw a flowchart.
     2. For editing, load saved data and then edit.
  3. For automatic generation:

     1. Specify the process flow to be generated and request automatic creation from generative AI.
     2. Manually adjust each element and connection of the automatically generated flowchart.
     3. Review the flowchart and edit it as needed.
  4. Save the completed flowchart data and image.
  5. Paste the image into your documents.

<img width="80%" src="example/作図想定フロー.png" />

## Limitations

* Canvas scrolling and zoom in/out are not supported yet (planned for future support).

## Notes

* Automatic flowchart generation uses the OpenAI API (GPT-5.2), so API usage fees will be incurred each time automatic generation is performed.

## Planned Features

* Optimization of the menu structure
* Canvas scrolling and zoom in/out
* Exporting drawn flowcharts to Excel
* Addition of more elements and swimlane drawing
* And more

## License

* This project is licensed under the MIT License.

## Changelog

* 2025/12/12 : Released basic features (provisional version)
* 2025/12/15 : Minor adjustments to link routing logic, added image export support (JPEG/PNG)
* 2025/12/15b: Updated README, added `requirements.txt`
* 2025/12/16 : Fixed an issue where node positions shifted when double-clicked
* 2025/12/16b: Added popup menu support, added confirmation dialog on tool exit
* 2025/12/16c: Updated README content and added images
* 2025/12/17 : Fixed a bug where some elements were not moved during multi-element movement
* 2025/12/19 : Added adjustable elements to definition files, added separate Japanese/English configuration examples, partially refactored source code
* 2025/12/24 : Added manual link routing adjustment (CTRL+MouseWheel: change connection points, SHIFT+MouseWheel: adjust routing offset)
* 2025/12/25 : Improved usability and created example tool usage videos
* 2025/12/27 : Added support for loading Mermaid-format data, adjusted label positions during manual link routing
* 2026/01/02 : Added support for automatic flowchart generation by integrating with generative AI (GPT-5.2)
