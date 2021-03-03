# Project Creator

Uses a GitHub repository as a template for a new project by downloading and extracting the repo zip into the current directory.

## Installation

`pip install "project_creator @ git+https://github.com/pwithams/project-creator"`

## Usage

Example using this repo as a template: https://github.com/pwithams/project-template

`project_creator init pwithams/project-template`

It will try download `master` branch by default. This can be changed:

`project_creator init pwithams/project-template --branch-name main`

Also supports:

`project_creator init https://github.com/pwithams/project-template`
`project_creator init https://github.com/pwithams/project-template.git`
