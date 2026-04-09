# flowchart-drawing-tool-python

**Simple Flowchart Drawing Tool (Python Version)** 

## Overview

This project provides a **“Simple Flowchart Drawing Tool (Python version)”** that allows users to easily create flowcharts.

## Project Purpose

* Have you ever experienced the following frustrations when creating flowcharts?

  * During the design phase, you want to quickly sketch flowcharts to organize business flows or processing logic, but you cannot find a suitable tool, making the task tedious.
  * You create flowcharts in Excel or PowerPoint for documentation, but it takes time to refine them, and re-editing due to logic changes or specification updates becomes exhausting.
  * In the era of generative AI, specifications tend to become text-heavy and hard to understand. Even when AI generates flowcharts, the results are often unsatisfactory and difficult to fine-tune.

* To address these common challenges, we created a **“casual and easy-to-use” flowchart drawing tool**.

* Since the tool now includes a sufficient set of basic features for quickly creating flowcharts, it has been released as open source.

* We hope it will be useful to as many people as possible.

## Features

* Quickly create, save, and re-edit simple flowcharts
* Automatic routing of links when connecting elements or moving nodes, with manual adjustment support
* Integration with generative AI (OpenAI GPT, Google Gemini, Anthropic Claude) for automatic flowchart generation (with manual editing available afterward)
* Supports both vertical and horizontal swimlanes
* **New Feature (2026.04.07)**: Released VBA for importing flowchart JSON data into Excel and rendering editable flowcharts → significantly reduces Excel diagramming workload

## Installation

### Prerequisites

* Supported OS: Verified on Windows 11 and macOS 26.4
* A Python execution environment with Tkinter Canvas support is required
  (Not supported in web environments such as Google Colab; macOS requires Tkinter setup)
* Git is recommended for checking out the latest code from GitHub

### Installation Steps

1. Open Command Prompt (or Terminal) and prepare a folder for checkout.

2. Move to the folder and clone the repository:

   ```
   git clone https://github.com/YoshiToshi1025/flowchart-drawing-tool-python.git
   ```

3. Install required packages:

   ```
   pip install -r requirements.txt
   ```

4. If you want to use English, overwrite `constants.py` with `constants_en.py`.

5. To use AI-based flow generation:

   * Set API keys in the `.env` file
   * Specify the AI model name in `constants.py`

   ```
   [.env]
   OPENAI_API_KEY=(OpenAI GPT API Key)
   GEMINI_API_KEY=(Google Gemini API Key)
   ANTHROPIC_API_KEY=(Anthropic Claude API Key)
   ```

   ```
   [constants.py]
   AI_MODEL="gpt-5.4"
   ```

   *Note: Manual flowchart creation works without API keys.*

6. Run `flowchart_tool.py` to launch the application.

## Usage

* **Placement**: Select elements (Swimlane, Process, Decision, Terminator, I/O, Storage, Document) from the menu and click on the canvas to place them.
* **Connection**: Select “Link” and click source → destination elements.
* **Text Editing**: Double-click elements or links.
* **Move**: Use “Select” and drag & drop elements.
* **Selection**:

  * Single: Click element
  * Multiple: Drag a rectangular area
* **Delete**: Remove selected elements and their links
* **UNDO/REDO**: Undo or redo recent actions
* **Import/Export**:

  * Export as image (JPEG/PNG) or JSON
  * Import JSON for redraw
* **Grid**: Enable grid snapping
* **AI Generation**:

  * Enable checkbox → enter flow → click Generate
* **Manual Link Adjustment**:

  * CTRL + MouseWheel: change connection points
  * SHIFT + MouseWheel: adjust routing distance
  * CTRL + SHIFT + MouseWheel: adjust label position

*Sample JSON files are available in the `example` folder.*

## Operation

### Expected Usage Flow

1. Launch the tool
2. For manual creation:

   * Create new flowchart OR load existing JSON
3. For AI generation:

   * Specify flow → generate → manually adjust layout and links
4. Save JSON and image
5. Import into Excel or embed image in documents

### Excel VBA Output

* Flowcharts can be automatically generated in Excel from JSON (manual adjustment still required for routing)

## Limitations

* On Windows, image saving may fail when multiple displays have different scaling settings → use screen capture instead
* Excel VBA import is **Windows-only** (macOS version under consideration)

## Notes

* Using AI generation incurs API usage costs depending on the selected AI service.

## Planned Features

* Enhancements for unsupported features in Excel VBA (Windows version)
* Excel VBA support for macOS
* More improvements

## License

* Licensed under the **MIT License**

## Changelog

* 2025/12/12: Initial release (basic features)
* 2025/12/15: Improved link routing, image export support
* 2025/12/16+: Various bug fixes and UI improvements
* 2026/01/02: AI integration (GPT-5.2)
* 2026/01/08: Display scaling support on Windows
* 2026/02/09: Node fill color customization
* 2026/03/03: Swimlane + highlight support
* 2026/03/17: Canvas resize and scroll support
* 2026/03/23: Straight links + dashed/dotted styles
* 2026/03/28: Multi-AI support (GPT, Gemini, Claude)
* 2026/04/06: JSON output update + Excel VBA beta
* 2026/04/07: Excel VBA (Windows) official release

## Notes (Additional)

### Note 1

If package errors occur:

```
pip install -r requirements.txt
```

### Note 2

* Excel VBA import works only on Windows

### Note 3

* Excel VBA works via import only (no additional setup required)
* Usage:

  * Run `DrawFlowchat` macro
  * Select JSON file
  * Auto-draw on active sheet
