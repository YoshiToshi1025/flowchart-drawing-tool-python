# flowchart-drawing-tool-python

Simple Flowchart Drawing Tool (Python Version)

## Overview

This project provides a **Simple Flowchart Drawing Tool (Python version)** that allows you to easily create flowcharts.

## Project Purpose

* Do you experience the following frustrations when creating flowcharts?

  * During requirement definition to detailed design, you want to use simple flowcharts to consider business processes and processing logic, but cannot find a tool that is both easy to draw and practical for real work—resulting in frustration every time you create a flowchart.
  * You create flowcharts in Excel or PowerPoint, but it takes a lot of time to adjust them into a satisfactory shape, and you get tired of re-adjusting layouts whenever the flowchart changes.
  * In the era of generative AI, specifications have become text-heavy. Even when you ask generative AI to create flowcharts, the results are unsatisfactory and cannot be easily edited.

* With these issues in mind, this tool was developed in Python with the goal of being a **casually usable flowchart drawing tool**.

* Since the basic functions required for drawing simple flowcharts are now in place, a provisional version is released.

* Note: Parts of the source code were generated using ChatGPT, and some areas are not yet well organized. These will be gradually cleaned up. 

* **New feature**: Integration with generative AI (GPT-5.2) to support automatic flowchart generation.
  (Manual adjustment of flowchart elements and link routing is still required.)

<img width="100%" src="example/flowchart_auto_generated_and_manual_edited.png" />

## Installation

### Prerequisites

* A Python-executable environment is required, with support for the Tkinter Canvas library.

  * This tool does **not** work in web-based environments such as Google Colaboratory.
  * On macOS, Tkinter must be properly enabled.

### Installation Steps

1. Check out this project’s code into a Python-capable environment.

2. In the checkout directory, run `pip install -r requirements.txt` to install required packages.

3. To automatically generate process flows using generative AI, create a `.env` file in the checkout directory and write your OpenAI API Key in the following format:
   (For instructions on obtaining an OpenAI API Key, refer to
   `"Docs/How_to_obtain_OpenAI_API_Key.md"`)

   ```
   OPENAI_API_KEY=(API Key obtained from OpenAI)
   ```

4. To use the tool in English, overwrite `constants.py` with `constants_en.py`.

5. Run `flowchart_tool.py` to launch the flowchart drawing tool.

## Usage

* **Placement**: Select Process, Decision, Terminator, or I/O from the menu, then click on the canvas to place an element.

  * **Available elements**

    * Terminator: Start, End, Subroutine
    * Process: Processing step
    * Decision: Branch
    * I/O: Input / Output

* **Connection**: Select *Link* from the menu, then select the source element followed by the destination element to draw a connection line.

* **Text editing**: Double-click an element or link on the canvas to enter text editing mode.

* **Move**: Select *Select* from the menu, then drag and drop elements on the canvas to move them.

* **Element selection**: Select *Select* from the menu and click an element to select it.

* **Multiple selection**: With *Select* active, drag a rectangular area starting from an empty space to select multiple elements.

* **Delete**: Click the *Delete* button in the menu to remove selected element(s) and their associated links.

* **UNDO / REDO**: Use the *UNDO* and *REDO* buttons in the menu to undo or redo the most recent edit operations.

* **Import / Export**: Export the canvas contents as an image (JPEG/PNG) or JSON file, or import a saved JSON file to redraw the flowchart.

* **Grid**: Enable the *Grid* checkbox to display a grid and constrain element placement to it.

* **Automatic flow generation**:
  Enable the *AI-generation* checkbox, specify the process flow to be generated in the right-side panel, and click the *Generate* button to automatically generate a flowchart.
  (Please manually adjust the layout after generation.)

* **Manual link routing adjustment**:
  When a link is selected:

  * `CTRL + Mouse Wheel`: Cycle through connection points
  * `SHIFT + Mouse Wheel`: Adjust detour distance
  * `CTRL + SHIFT + Mouse Wheel`: Cycle through label position

* Sample JSON files are provided in the `example` folder. These can be loaded using **[Load JSON]**.

## Operation

* The current provisional version assumes the following workflow:

  1. Launch the flowchart drawing tool
  2. For manual creation:

     1. Create a new flowchart, or
     2. Load saved data and edit it
  3. For automatic generation:

     1. Specify the process flow to be generated and request automatic generation via generative AI
     2. Manually adjust each generated element and link
     3. Review the flowchart and edit as necessary
  4. Save the completed flowchart data and images
  5. Paste the images into documentation

## Limitations

* Canvas scrolling and zoom in/out are not supported yet (under consideration).
* On Windows, if multiple displays use different scaling settings, the “Save Image” function may not work correctly. In such cases, please use a screen capture tool instead.

## Notes

* Automatic flowchart generation uses the OpenAI API (GPT-5.2).
  API usage fees will be incurred each time automatic generation is performed.

## Planned Features

* Optimization of menu structure
* Canvas scrolling and zoom in/out
* Export of drawn flowcharts to Excel
* Additional elements and swimlane drawing
* And more

## License

* This project is licensed under the **MIT License**.

## Change Log

* 2025/12/12: Released basic functionality (provisional version)
* 2025/12/15: Fine-tuned link routing logic, added image export (JPEG/PNG)
* 2025/12/15b: Updated README, added requirements.txt
* 2025/12/16: Fixed issue where node positions shifted on double-click
* 2025/12/16b: Added popup menu support, confirmation dialog on exit
* 2025/12/16c: Updated README and added images
* 2025/12/17: Fixed bug where some elements did not move during multi-selection moves
* 2025/12/19: Added adjustable elements to config files, added Japanese/English configuration examples, partially refactored source code
* 2025/12/24: Added manual link routing adjustment
  (CTRL+MouseWheel: change connection point, SHIFT+MouseWheel: adjust detour distance)
* 2025/12/25: Improved usability, created tool usage video examples
* 2025/12/27: Added support for importing Mermaid-format data, adjusted label positions during manual link routing
* 2026/01/02: Added automatic flowchart generation via generative AI (GPT-5.2)
* 2026/01/05: Added rough automatic layout for AI-generated flows (manual adjustment still required)
* 2026/01/08: Support for image export when Windows display scaling is not set to 100%, and definition of shortcut keys
* 2026/01/09 : Display adjustment on MacOS
* 2026/01/13 : Bug fixes (generative AI integration, file dialog configuration)
* 2026/01/19 : Supports manual adjustment of link label positions
* 2026/01/27 : Supports link routing pattern (Bottom to Top, 5 lines)
* 2026/01/30 : Support for link arrow definitions (shape and direction), support for line breaks(\n) in label text, and bug fixes (manual adjustment of link label positions).
