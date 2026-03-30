# flowchart-drawing-tool-python

Simple Flowchart Drawing Tool (Python Version)

## Overview

This project provides a **Simple Flowchart Drawing Tool (Python version)** that allows you to easily create flowcharts.

## Project Purpose

* When creating a flowchart, have you ever experienced frustrations like the following?

  * During the design phase, when examining business workflows or processing logic, you want to quickly sketch a simple flowchart to organize your thoughts. However, you cannot find a suitable tool, and creating flowcharts ends up feeling unnecessarily cumbersome.
  * You create flowcharts in Excel or PowerPoint to include in design documents, but it takes a long time to arrange them into a satisfactory format. On top of that, repeated edits caused by logic changes or specification updates become tedious and frustrating.
  * In the era of generative AI, specifications often become long documents filled with text, making them difficult to understand. Even when you ask generative AI to draw a flowchart, the result is often unsatisfactory, and you cannot easily make small adjustments, which can be quite frustrating.

* For people who share these common challenges, I created a “casual and easy-to-use” flowchart drawing tool.

* Since the tool now includes a reasonable set of basic features for quickly sketching flowcharts, I am releasing it as open source.

* I hope it will be useful to as many people as possible.

<div style="text-align: center;">
<img width="75%" src="example/フローチャート自動生成＆手動調整後_jp.png" />
</div>

## Features of This Tool

* Create, save, and re-edit simple flowcharts quickly

* Automatic link routing between elements, with links automatically updated when elements are moved. Manual routing adjustments are also supported.

* Integration with generative AI (GPT, Gemini, Claude) to automatically generate flowcharts (manual editing is possible after generation)

* Swimlane diagram support

<div style="text-align: center;">
<img width="75%" src="example/商品注文対応フロー.png" />
</div>

<div style="text-align: center;">
<img width="75%" src="example/設計作業承認フロー図_ステータス付.png" />
</div>

## Installation

* **Prerequisites**

  * Supported OS: Verified to run on Windows 11 and macOS 26.4
  * A Python runtime environment is required, along with support for the Tkinter Canvas library.
    (Not supported in web environments such as Google Colaboratory. On macOS, Tkinter must be properly configured.)
  * It is recommended to use the `git` command to check out the latest code from GitHub.

* **Installation Steps**

  1. Launch Command Prompt (or Terminal) and prepare a folder for checkout.
  2. Navigate to the checkout folder and clone this project from GitHub:

     ```
     git clone https://github.com/YoshiToshi1025/flowchart-drawing-tool-python.git
     ```
  3. In the checkout folder, run the following command to install the required packages:

     ```
     pip install -r requirements.txt
     ```
  4. If you want to use the tool in English, overwrite `constants.py` with `constants_en.py`.
  5. If you want to enable AI-based flow generation, add the API key of your preferred generative AI to the `.env` file in the checkout folder, and specify the AI model name in the configuration file (`constants.py`).
     *Note: You can still use the tool for manual flowchart creation without setting an API key.*

     ```
     [.env file]
     OPENAI_API_KEY=(API key for OpenAI GPT)
     GEMINI_API_KEY=(API key for Google Gemini)
     ANTHROPIC_API_KEY=(API key for Anthropic Claude)
     ```

     ```
     [constants.py file]
     AI_MODEL=Name of the generative AI model to use
     Example) AI_MODEL="gpt-5.4"
     ```
  6. Run `flowchart_tool.py` to launch the flowchart drawing tool.

## Usage

* **Placement**: Select Process, Decision, Terminator, I/O, Storage or Document from the menu, then click on the canvas to place an element.

  * **Available elements**

    * Swimlane: Swimlane
    * Terminator: Start, End, Subroutine
    * Process: Processing step
    * Decision: Branch
    * I/O: Input / Output
    * Storage: Storage
    * Document: Document

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

<div style="text-align: center;">
<img width="75%" src="example/作図想定フロー.png" />
</div>

## Limitations

* Canvas zoom in/out are not supported yet (under consideration).
* On Windows, if multiple displays use different scaling settings, the “Save Image” function may not work correctly. In such cases, please use a screen capture tool instead.

## Notes

* Automatic flowchart generation uses the Generative AI API (OpenAI GPT, Google Gemini, Anthropic Claude).
  API usage fees will be incurred each time automatic generation is performed.

## Planned Features

* Canvas scrolling and zoom in/out
* Export of drawn flowcharts to Excel
* Additional elements
* And more

## License

* This project is licensed under the **MIT License**.

## Change Log

* 2025/12/12 : Released basic functionality (provisional version)
* 2025/12/15 : Fine-tuned link routing logic, added image export (JPEG/PNG)
* 2025/12/15b: Updated README, added requirements.txt
* 2025/12/16 : Fixed issue where node positions shifted on double-click
* 2025/12/16b: Added popup menu support, confirmation dialog on exit
* 2025/12/16c: Updated README and added images
* 2025/12/17 : Fixed bug where some elements did not move during multi-selection moves
* 2025/12/19 : Added adjustable elements to config files, added Japanese/English configuration examples, partially refactored source code
* 2025/12/24 : Added manual link routing adjustment (CTRL+MouseWheel: change connection point, SHIFT+MouseWheel: adjust detour distance)
* 2025/12/25 : Improved usability, created tool usage video examples
* 2025/12/27 : Added support for importing Mermaid-format data, adjusted label positions during manual link routing
* 2026/01/02 : Added automatic flowchart generation via generative AI (GPT-5.2)
* 2026/01/05 : Added rough automatic layout for AI-generated flows (manual adjustment still required)
* 2026/01/08 : Support for image export when Windows display scaling is not set to 100%, and definition of shortcut keys
* 2026/01/09 : Display adjustment on MacOS
* 2026/01/13 : Bug fixes (generative AI integration, file dialog configuration)
* 2026/01/19 : Supports manual adjustment of link label positions
* 2026/01/27 : Supports link routing pattern (Bottom to Top, 5 lines)
* 2026/01/30 : Support for link arrow definitions (shape and direction), support for line breaks(\n) in label text, and bug fixes (manual adjustment of link label positions).
* 2026/02/03 : Definition of mouse wheel operations, ability to select rounded rectangles for Process shapes, and improved link selection operations
* 2026/02/09 : Added support for manually changing node fill colors.
* 2026/03/03 : Supports swimlane display and node highlight/non-highlight display.
* 2026/03/07 : Improved the menu structure, updated the default AI integration to GPT-5.4, and refined the source code implementation.
* 2026/03/17 : Added support for canvas resizing and scrolling.
* 2026/03/23 : Added support for straight-line links, and enabled changing the line style of straight-line links from solid to dotted or dashed.
* 2026/03/24 : Supports storage and document diagram creation.
* 2026/03/25 : Added support for creating an operation manual (Japanese, HTML) and accessing it from the toolbar.
* 2026/03/28 : With the generative AI integration feature, it is now possible to specify not only OpenAI but also Gemini or Claude. (Configure the API key in the .env file and select the model in AI_MODEL within constants.py.)
* 2026/03/30 : Updated the README and the user manual (HTML, Japanese).

## Additional Notes
* If package errors occur, please try installing all packages at once using the following command.
* $ pip install -r requirements.txt
