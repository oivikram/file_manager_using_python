# File Manager Web App

This project converts the original Python CLI file manager into a minimal full-stack web app.

- Backend: FastAPI
- Frontend: React + Vite
- Communication: JSON REST API
- Storage scope: only inside the `data/` folder at the project root

## Project Tree

```text
file_handdling/
|-- backend/
|   |-- app.py
|   `-- requirements.txt
|-- frontend/
|   |-- package.json
|   |-- vite.config.js
|   |-- index.html
|   `-- src/
|       |-- App.jsx
|       |-- main.jsx
|       `-- styles.css
|-- data/
|-- main.py
|-- python.py
`-- README.md
```

## Features

- List files and folders recursively inside `data/`
- Create a file with initial content
- Read file content
- Append content with a leading newline
- Delete a file

## Security Rules

- Rejects invalid paths such as `../secret.txt`
- Rejects paths that escape the `data/` directory
- Only performs read, append, and delete operations on regular files
- Uses UTF-8 for all file reads and writes
- Returns JSON errors with proper HTTP status codes

## Backend API

### `GET /api/items`

Returns:

```json
{
	"items": [
		{ "path": "notes.txt", "type": "file" },
		{ "path": "docs", "type": "dir" }
	]
}
```

### `POST /api/files`

Request body:

```json
{
	"name": "notes/today.txt",
	"content": "hello"
}
```

### `GET /api/files/{name}`

Response:

```json
{
	"name": "notes/today.txt",
	"content": "hello"
}
```

### `POST /api/files/{name}/append`

Request body:

```json
{
	"content": "more text"
}
```

### `DELETE /api/files/{name}`

Response:

```json
{
	"message": "File deleted successfully",
	"name": "notes/today.txt"
}
```

## How To Run

### Backend (Windows PowerShell)

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
uvicorn backend.app:app --reload
```

Backend will run at `http://127.0.0.1:8000`.

### Frontend (Windows PowerShell)

Open a second terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Frontend will run at `http://127.0.0.1:5173`.

## Quick Manual Test Steps

Create a file:

```powershell
curl -Method POST http://127.0.0.1:8000/api/files \
	-Headers @{"Content-Type"="application/json"} \
	-Body '{"name":"notes.txt","content":"hello"}'
```

List items:

```powershell
curl http://127.0.0.1:8000/api/items
```

Read a file:

```powershell
curl http://127.0.0.1:8000/api/files/notes.txt
```

Append to a file:

```powershell
curl -Method POST http://127.0.0.1:8000/api/files/notes.txt/append \
	-Headers @{"Content-Type"="application/json"} \
	-Body '{"content":"second line"}'
```

Delete a file:

```powershell
curl -Method DELETE http://127.0.0.1:8000/api/files/notes.txt
```

## Original CLI Script

The original CLI implementation is still present in `main.py` for reference. The new web app moves that behavior into API endpoints and a browser UI.
