# Voicense API Documentation

## Introduction
This document outlines the endpoints and functionalities of the Voicense API.

## IDs of Each Entity
- **User**: `VCSS0001` or `VCSL0002`
- **Note**: `VCSN0003`
- **Module**: `VCSM0004`
- **Transcription**: `VCST0005`

## Endpoints

### Root
- **Method**: GET
- **Description**: Root entry point for landing page.

### Authentication
#### Login
- **Endpoint**: /auth/login
- **Method**: POST
- **Description**: Send encrypted username and password to authenticate user.
- **Return**: Valid user or not.

#### Signup
- **Endpoint**: /auth/signup
- **Method**: POST
- **Description**: Send user object to register in the system with validation.
- **Return**: User registered or not.

### Note
#### Recent Notes
- **Endpoint**: /note/recent
- **Method**: GET
- **Description**: Return list of recent lecture note card objects.
- **Note**: Provides note view cards, not the full note content.

#### Search Notes
- **Endpoint**: /note/search
- **Method**: POST
- **Description**: Send entered text in search box to find relevant lecture note card list.
- **Return**: Lecture note card list.

#### Get Note by ID
- **Endpoint**: /note/{note_id}
- **Method**: GET
- **Description**: Return note content relevant to note_id.
- **Note**: Note content is in .md file format.

#### Trash Note
- **Endpoint**: /note/trash/{note_id}
- **Method**: DELETE
- **Description**: Trash the relevant note.
- **Return**: Successful or not.

#### Share Note
- **Endpoint**: /note/share/{note_id}
- **Method**: POST
- **Description**: Return the sharable link of the note.

### Module
#### Get All Modules
- **Endpoint**: /module/all
- **Method**: GET
- **Description**: Return all modules when record icon clicked.

#### Search Modules
- **Endpoint**: /module/search
- **Method**: POST
- **Description**: Send entered text in search box to find relevant module card list.
- **Return**: Relevant module card list.

#### Share Module
- **Endpoint**: /module/share/{module_id}
- **Method**: GET
- **Description**: Return sharable link of the module.

#### Trash Module
- **Endpoint**: /module/trash/{module_id}
- **Method**: DELETE
- **Description**: Trash the relevant module.
- **Return**: Success or not.

#### Get Notes by Module ID
- **Endpoint**: /module/{module_id}/notes
- **Method**: POST
- **Description**: When module card clicked, send the id to get all note card list of the module.

#### Get Other Notes
- **Endpoint**: /module/other/notes
- **Method**: GET
- **Description**: Return list of non-module note card notes.

#### Add Module
- **Endpoint**: /module/add
- **Method**: POST
- **Description**: Send module name to add a new module.
- **Return**: Success or not.

#### Edit Module
- **Endpoint**: /module/edit/{module_id}
- **Method**: POST
- **Description**: Send module id with new name to edit the module.
- **Return**: Success or not.

### Record
#### Upload Recording
- **Endpoint**: /record/upload
- **Method**: POST
- **Description**: When stop button clicked, upload the lecture recording to the database with relevant details.
- **Return**: Upload successful message for notification.
