import { useEffect, useState } from 'react';


const API_BASE_URL = 'http://127.0.0.1:8000';


async function parseResponse(response) {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || 'Request failed');
  }

  return data;
}


export default function App() {
  const [items, setItems] = useState([]);
  const [fileName, setFileName] = useState('');
  const [content, setContent] = useState('');
  const [message, setMessage] = useState('Ready');
  const [isError, setIsError] = useState(false);

  async function refreshItems() {
    try {
      const data = await parseResponse(await fetch(`${API_BASE_URL}/api/items`));
      setItems(data.items);
      setMessage('Items refreshed');
      setIsError(false);
    } catch (error) {
      setMessage(error.message);
      setIsError(true);
    }
  }

  useEffect(() => {
    refreshItems();
  }, []);

  async function createFile() {
    try {
      const data = await parseResponse(
        await fetch(`${API_BASE_URL}/api/files`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: fileName, content }),
        })
      );
      setMessage(data.message);
      setIsError(false);
      await refreshItems();
    } catch (error) {
      setMessage(error.message);
      setIsError(true);
    }
  }

  async function readFile() {
    try {
      const encodedName = fileName
        .split('/')
        .map((segment) => encodeURIComponent(segment))
        .join('/');
      const data = await parseResponse(
        await fetch(`${API_BASE_URL}/api/files/${encodedName}`)
      );
      setContent(data.content);
      setMessage(`Loaded ${data.name}`);
      setIsError(false);
    } catch (error) {
      setMessage(error.message);
      setIsError(true);
    }
  }

  async function appendFile() {
    try {
      const encodedName = fileName
        .split('/')
        .map((segment) => encodeURIComponent(segment))
        .join('/');
      const data = await parseResponse(
        await fetch(`${API_BASE_URL}/api/files/${encodedName}/append`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content }),
        })
      );
      setMessage(data.message);
      setIsError(false);
      await refreshItems();
    } catch (error) {
      setMessage(error.message);
      setIsError(true);
    }
  }

  async function deleteFile() {
    try {
      const encodedName = fileName
        .split('/')
        .map((segment) => encodeURIComponent(segment))
        .join('/');
      const data = await parseResponse(
        await fetch(`${API_BASE_URL}/api/files/${encodedName}`, {
          method: 'DELETE',
        })
      );
      setContent('');
      setMessage(data.message);
      setIsError(false);
      await refreshItems();
    } catch (error) {
      setMessage(error.message);
      setIsError(true);
    }
  }

  return (
    <main className="app-shell">
      <section className="panel">
        <h1>File Manager</h1>
        <p className="subtle">All operations are limited to the backend data folder.</p>

        <div className="form-row">
          <label htmlFor="fileName">File name</label>
          <input
            id="fileName"
            value={fileName}
            onChange={(event) => setFileName(event.target.value)}
            placeholder="example.txt or notes/today.txt"
          />
        </div>

        <div className="form-row">
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            rows="8"
            value={content}
            onChange={(event) => setContent(event.target.value)}
            placeholder="Type file content here"
          />
        </div>

        <div className="button-row">
          <button type="button" onClick={createFile}>Create</button>
          <button type="button" onClick={readFile}>Read</button>
          <button type="button" onClick={appendFile}>Append</button>
          <button type="button" onClick={deleteFile}>Delete</button>
          <button type="button" onClick={refreshItems}>Refresh list</button>
        </div>

        <div className={isError ? 'message error' : 'message'}>{message}</div>
      </section>

      <section className="panel">
        <h2>Items in data/</h2>
        <ul className="item-list">
          {items.length === 0 ? <li>No files or folders yet.</li> : null}
          {items.map((item) => (
            <li key={`${item.type}:${item.path}`}>
              <span className="item-type">[{item.type}]</span> {item.path}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
