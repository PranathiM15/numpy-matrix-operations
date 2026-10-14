'use strict';

const sampleA = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
const sampleB = [[9, 8, 7], [6, 5, 4], [3, 2, 1]];
let selectedOperation = 'add';
let toastTimer;

const operationNames = {
  add: 'addition',
  subtract: 'subtraction',
  multiply: 'matrix multiplication',
  transpose_a: 'transpose A',
  transpose_b: 'transpose B'
};
const equations = {add: 'A + B', subtract: 'A − B', multiply: 'A × B', transpose_a: 'Aᵀ', transpose_b: 'Bᵀ'};

function renderEditor(id, data, prefix) {
  const parent = document.getElementById(id);
  parent.replaceChildren();
  parent.style.gridTemplateColumns = `repeat(${data[0].length}, minmax(0, 1fr))`;
  data.forEach((row, r) => row.forEach((value, c) => {
    const input = document.createElement('input');
    input.className = 'matrix-cell';
    input.type = 'number';
    input.step = 'any';
    input.value = value;
    input.inputMode = 'decimal';
    input.autocomplete = 'off';
    input.setAttribute('aria-label', `Matrix ${prefix}, row ${r + 1}, column ${c + 1}`);
    input.dataset.row = String(r);
    input.dataset.col = String(c);
    input.addEventListener('input', () => input.classList.remove('invalid'));
    parent.appendChild(input);
  }));
}

function readEditor(id, label) {
  const inputs = [...document.querySelectorAll(`#${id} input` )];
  const matrix = [];
  let valid = true;
  inputs.forEach(input => {
    const value = input.value.trim();
    const number = Number(value);
    const ok = value !== '' && Number.isFinite(number);
    input.classList.toggle('invalid', !ok);
    valid = valid && ok;
    const r = Number(input.dataset.row);
    matrix[r] ??= [];
    matrix[r][Number(input.dataset.col)] = number;
  });
  if (!valid) throw new Error(`${label}: enter a finite number in every cell.`);
  return matrix;
}

function showToast(message, isError = false) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.toggle('error', isError);
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3200);
}

function displayResult(payload) {
  const body = document.getElementById('result-body');
  body.replaceChildren();
  const wrapper = document.createElement('div');
  wrapper.className = 'result-matrix-wrap';
  const matrix = document.createElement('div');
  matrix.className = 'result-matrix';
  matrix.style.setProperty('--cols', payload.shape[1]);
  payload.result.flat().forEach(value => {
    const cell = document.createElement('div');
    cell.className = 'result-value';
    cell.textContent = typeof value === 'number' ? String(Number(value.toPrecision(10))) : String(value);
    matrix.appendChild(cell);
  });
  const meta = document.createElement('div');
  meta.className = 'result-meta';
  [`${payload.shape[0]} × ${payload.shape[1]} result`, 'Calculated with NumPy', `np.${payload.operation}`].forEach(text => {
    const chip = document.createElement('span');
    chip.className = 'meta-chip';
    chip.textContent = text;
    meta.appendChild(chip);
  });
  wrapper.append(matrix, meta);
  const explanation = document.createElement('p');
  explanation.className = 'result-explanation';
  explanation.textContent = payload.explanation;
  body.append(wrapper, explanation);
  document.getElementById('result-equation').textContent = payload.title;
  const badge = document.getElementById('result-badge');
  badge.textContent = 'CALCULATION COMPLETE';
  badge.classList.add('ready');
  const note = document.querySelector('#result-note p');
  note.textContent = payload.operation === 'multiply'
    ? 'Matrix multiplication combines a row from A with a column from B. Every output cell is the sum of pairwise products; it is not the same as element-wise multiplication.'
    : payload.operation.startsWith('transpose')
      ? 'A transpose swaps the row and column axes. The number of rows in the result equals the original number of columns, and vice versa.'
      : 'Addition and subtraction work element by element, so both matrices must have matching dimensions.';
}

async function compute() {
  const button = document.getElementById('compute-button');
  let matrixA, matrixB;
  try {
    matrixA = readEditor('matrix-a', 'Matrix A');
    matrixB = readEditor('matrix-b', 'Matrix B');
  } catch (error) {
    showToast(error.message, true);
    return;
  }
  button.disabled = true;
  button.innerHTML = 'Calculating… <span aria-hidden="true">◌</span>';
  try {
    const response = await fetch('/api/compute', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({matrix_a: matrixA, matrix_b: matrixB, operation: selectedOperation})
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'Calculation failed.');
    displayResult(payload);
  } catch (error) {
    showToast(error.message || 'Could not reach the Python server. Is it running?', true);
  } finally {
    button.disabled = false;
    button.innerHTML = 'Run calculation <span aria-hidden="true">↗</span>';
  }
}

document.querySelectorAll('.operation-button').forEach(button => {
  button.addEventListener('click', () => {
    selectedOperation = button.dataset.operation;
    document.querySelectorAll('.operation-button').forEach(item => item.classList.toggle('active', item === button));
    document.getElementById('selected-operation').textContent = operationNames[selectedOperation];
    document.getElementById('result-equation').textContent = equations[selectedOperation];
  });
});

document.getElementById('compute-button').addEventListener('click', compute);
document.getElementById('reset-button').addEventListener('click', () => {
  renderEditor('matrix-a', sampleA, 'A');
  renderEditor('matrix-b', sampleB, 'B');
  document.getElementById('result-body').innerHTML = '<div class="empty-result"><div class="empty-icon">[ ]</div><h3>Your answer will appear here</h3><p>Choose an operation and press <strong>Run calculation</strong> to see the NumPy result.</p></div>';
  document.getElementById('result-badge').textContent = 'AWAITING RUN';
  document.getElementById('result-badge').classList.remove('ready');
  document.getElementById('result-equation').textContent = equations[selectedOperation];
  document.querySelector('#result-note p').textContent = 'Tip: use square matrices for this sample so that every operation is available. Matrix multiplication requires the number of columns in A to match the number of rows in B.';
  showToast('Sample matrices restored.');
});

renderEditor('matrix-a', sampleA, 'A');
renderEditor('matrix-b', sampleB, 'B');
