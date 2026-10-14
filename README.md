# Matrix Studio — NumPy Matrix Operations (Task 14)

A small, responsive web application for the Veda Technology AI & ML Track Task 14. It lets a learner edit two matrices and calculate addition, subtraction, matrix multiplication, and the transpose of either matrix. The browser sends values to a Python endpoint, where **NumPy** performs the calculations.

## Features

- Editable sample matrices A and B, with a one-click restore button.
- Addition (`np.add`), subtraction (`np.subtract`), matrix multiplication (`np.matmul` / `A @ B`), and transpose (`A.T`, `B.T`).
- Clear explanations, matrix dimensions, validation messages, and a responsive interface.
- Uses Python's standard-library HTTP server: no Flask, Django, Node.js, or notebook is needed.
- Includes automated unit tests, a Render deployment blueprint, a Procfile, and rollback guidance.

## Tools used

- Python 3.10 or newer (Python 3.12 recommended)
- NumPy
- HTML, CSS, and JavaScript for the browser interface
- Python `unittest` and built-in `http.server` (both included with Python)

## Run on Windows PowerShell (no notebook, no activation required)

1. Download and extract the ZIP. Open the extracted `numpy-matrix-operations` folder in File Explorer.
2. Click the folder address bar, type `powershell`, and press Enter. PowerShell opens directly in the project folder.
3. Check Python and Git are installed:

   ```powershell
   py --version
   git --version
   ```

4. Create a virtual environment and install NumPy. These commands call the environment's Python directly, so you do **not** need to run `Activate.ps1` or change PowerShell execution policy:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. Run the tests:

   ```powershell
   .\.venv\Scripts\python.exe -m unittest discover -s tests -v
   ```

   You should see `OK` at the end.

6. Start the website:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

7. Open **http://127.0.0.1:8000** in Chrome or Edge. Edit matrix cells, select an operation, and click **Run calculation**. Keep the PowerShell window open while using the app. To stop it, press **Ctrl+C**.

### If Python commands are not recognized

Install Python 3 from [python.org](https://www.python.org/downloads/windows/) and select **Add python.exe to PATH** during installation. Close and reopen PowerShell. If `py` is unavailable but `python --version` works, replace `py` in the virtual-environment command with `python`.

### Quick sample check

The initial matrices are:

```text
A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
```

- `A + B`: all entries are `10`.
- `A - B`: `[[-8, -6, -4], [-2, 0, 2], [4, 6, 8]]`.
- `A @ B`: `[[30, 24, 18], [84, 69, 54], [138, 114, 90]]`.
- `A.T`: `[[1, 4, 7], [2, 5, 8], [3, 6, 9]]`.

## Push to your GitHub account

Your supplied screenshot shows the GitHub username `PranathiM15`. Create the repository from [github.com/new](https://github.com/new):

1. Repository name: `numpy-matrix-operations`.
2. Choose **Public**.
3. Leave **Add a README**, `.gitignore`, and license unchecked because these files are already in this project.
4. Click **Create repository**. Keep the page open for the remote URL.
5. In the same PowerShell window opened in this project folder, run:

   ```powershell
   git init
   git branch -M main
   git add .
   git status
   git commit -m "Build NumPy matrix operations web app"
   git remote add origin https://github.com/PranathiM15/numpy-matrix-operations.git
   git push -u origin main
   ```

6. If Git asks you to sign in, finish the browser/Git Credential Manager prompt. Do not paste a GitHub password or token into this README or commit one to the project.
7. Open `https://github.com/PranathiM15/numpy-matrix-operations` and check that `app.py`, `matrix_ops.py`, `static/`, and `README.md` appear.

**If Git says `remote origin already exists`:**

```powershell
git remote set-url origin https://github.com/PranathiM15/numpy-matrix-operations.git
git push -u origin main
```

**If `git commit` says your identity is unknown**, configure it once with the name/email you want on commits, then retry the commit:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
git commit -m "Build NumPy matrix operations web app"
```

Do not run `git init` from a parent directory; commands should be run in the extracted project root, where this README and `app.py` are located.

## Deployment configuration (Render)

A `render.yaml` Blueprint and `Procfile` are included. They specify `pip install -r requirements.txt`, `python app.py`, and `/health` as the health-check endpoint.

1. Push the project to GitHub first.
2. Sign in to [Render](https://render.com/) and choose **New → Blueprint** (or create a **Web Service** connected to the repository).
3. Select `PranathiM15/numpy-matrix-operations`. If creating a Web Service manually, use runtime **Python**, build command `pip install -r requirements.txt`, start command `python app.py`, and health-check path `/health`.
4. Start the deployment and wait for the build and health check to succeed. Open the public URL shown by Render and try one addition and one multiplication.
5. Add the live URL and deployment date to your submission notes after it is actually live. A deployment is not created automatically by uploading this ZIP to GitHub.

Render's current Blueprint and Web Service references: [Blueprint YAML](https://render.com/docs/blueprint-spec) and [Web Services](https://render.com/docs/web-services).

## Rollback and evidence

Read [`ROLLBACK.md`](ROLLBACK.md) and use [`evidence/ROLLBACK_EVIDENCE_TEMPLATE.md`](evidence/ROLLBACK_EVIDENCE_TEMPLATE.md) to record what you actually did. No real GitHub push, hosting deployment, or production rollback has been run as part of generating this starter ZIP, so the template is intentionally not marked as completed evidence.

Safe rollback for a code change is normally performed with `git revert <bad-commit-hash>` and then `git push origin main`; this preserves history. For a hosting issue, open the service's deployment history and redeploy the last known-good deployment if the platform offers that option. After rollback, check `/health` and test addition and multiplication again. Record the real commit/deployment IDs, time, and screenshots in the evidence template.

## Interview questions

**What is a matrix?** A rectangular arrangement of numerical values organized in rows and columns.

**What is the difference between element-wise and matrix multiplication?** Element-wise multiplication multiplies values at matching positions. Matrix multiplication uses row-column dot products and requires the first matrix's column count to equal the second matrix's row count.

**Why are matrices important in machine learning?** They efficiently represent datasets, feature vectors, weights, and transformations, and vectorized array operations help numerical workloads run efficiently.

## Project structure

```text
numpy-matrix-operations/
├── app.py
├── matrix_ops.py
├── requirements.txt
├── Procfile
├── render.yaml
├── README.md
├── ROLLBACK.md
├── .gitignore
├── static/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
│   └── test_matrix_ops.py
└── evidence/
    └── ROLLBACK_EVIDENCE_TEMPLATE.md
```
