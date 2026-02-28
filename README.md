<h1 align="center"><b>Hybrid Log Classification System</b></h1>

<p align="center">
  A practical, cost-aware log classification pipeline that turns messy logs into consistent categories for faster triage
  (critical errors, security alerts, system notifications, user actions, etc.).
</p>

<hr />

<h2>📌 Overview</h2>
<ul>
  <li><b>Goal:</b> Automatically classify logs into meaningful categories to improve readability, monitoring, and incident response.</li>
  <li><b>Approach:</b> A hybrid pipeline combining <b>Regex</b>, <b>BERT embeddings</b>, and an <b>LLM</b> fallback.</li>
  <li><b>Why hybrid?</b> Regex is fast + free, embeddings are accurate for known patterns, and LLM handles low-data / high-variance cases.</li>
</ul>

<h2>🧠 What This System Does</h2>
<p>
Given a log record <code>(source, log_message)</code>, the system routes the message through a cost-efficient decision tree:
</p>

<ol>
  <li>
    <b>Regex Classification (fastest / cheapest)</b>
    <ul>
      <li>Runs the message through curated regex rules built from recurring log patterns.</li>
      <li>If a match is found → return a label immediately.</li>
    </ul>
  </li>

  <li>
    <b>Fallback Path</b> (if regex cannot classify)
    <ul>
      <li>
        If the system has <b>enough training samples</b> for that type of log → use <b>BERT embedding classification</b>
        (SentenceTransformer embeddings + Logistic Regression).
      </li>
      <li>
        If the log type has <b>insufficient training samples</b> (low-data) → use an <b>LLM classifier</b> (Groq).
      </li>
    </ul>
  </li>
</ol>

<p>
This hybrid design helps balance:
</p>
<ul>
  <li><b>Cost:</b> Avoids LLM calls for predictable logs</li>
  <li><b>Accuracy:</b> Uses ML for complex patterns not captured by regex</li>
  <li><b>Scalability:</b> Regex covers the most common patterns while ML/LLM handles the long tail</li>
</ul>

<hr />

<h2>🔬 Training Workflow (Jupyter Notebook)</h2>
<ol>
  <li><b>Load dataset</b> into a DataFrame</li>
  <li><b>Remove</b> the <code>complexity</code> column (not needed for training)</li>
  <li><b>Vectorize</b> log messages using <b>SentenceTransformer</b> (embeddings)</li>
  <li><b>Cluster</b> embeddings using <b>DBSCAN</b></li>
  <li><b>Inspect clusters</b> and identify groups with consistent / repetitive messages</li>
  <li><b>Build regex rules</b> from highly consistent clusters</li>
  <li><b>Find unclassified logs</b> (not matched by regex)</li>
  <li><b>Sample-size rule:</b> determine whether to use ML vs LLM for the remaining logs</li>
  <li><b>Train Logistic Regression</b> on embedding vectors for labels with sufficient samples</li>
  <li><b>Persist model</b> to disk with <code>joblib</code></li>
</ol>

<p>
<b>Sample-size logic:</b> Labels with fewer than a threshold (e.g., 5 samples) are treated as low-data and routed to the LLM.
</p>

<hr />

<h2>🏗️ Project Structure (PyCharm)</h2>
<p>
The project is split into a main orchestrator and dedicated processors for each classification method:
</p>

<ul>
  <li><code>classify.py</code> — Hybrid routing logic (LLM vs Regex vs Embedding classifier)</li>
  <li><code>processor_regex.py</code> — Regex rules and regex-based classification</li>
  <li><code>processor_bert.py</code> — SentenceTransformer embedding + sklearn classifier inference</li>
  <li><code>processor_llm.py</code> — Groq LLM integration for low-data classifications</li>
  <li><code>server.py</code> — FastAPI backend that accepts CSV uploads and returns classified output</li>
  <li><code>models/</code> — Saved sklearn model artifacts (<code>.joblib</code>)</li>
  <li><code>resources/</code> — Test CSV inputs and generated outputs</li>
</ul>

<hr />

<h2>🤖 Embedding + ML Classification (BERT)</h2>
<ul>
  <li>Uses <b>SentenceTransformer</b> to convert log messages into dense vectors.</li>
  <li>Runs vectors through a trained <b>Logistic Regression</b> classifier.</li>
  <li>
    Includes a safety rule:
    <ul>
      <li>If confidence is below a threshold (e.g., <code>max(prob) &lt; 0.5</code>) → return <code>Unclassified</code></li>
    </ul>
  </li>
</ul>

<hr />

<h2>🧾 LLM Classification (Groq)</h2>
<ul>
  <li>Low-data logs (insufficient training samples) are classified using a Groq-hosted LLM.</li>
  <li>API key is stored securely via environment variables (recommended via <code>.env</code>).</li>
  <li>A structured prompt is used to map messages into the same target label set as regex/ML.</li>
</ul>

<hr />

<h2>🌐 FastAPI Backend</h2>
<p>
A simple API that accepts a CSV upload and returns the classified CSV.
</p>

<h3>Endpoint</h3>
<pre><code>POST /classify/</code></pre>

<h3>Input CSV Requirements</h3>
<ul>
  <li>Must contain columns: <code>source</code>, <code>log_message</code></li>
</ul>

<h3>Output</h3>
<ul>
  <li>Returns a CSV including a new <code>target_label</code> column</li>
</ul>

<h3>Testing</h3>
<ul>
  <li>Tested via Postman using <code>multipart/form-data</code> upload with key <code>file</code></li>
</ul>

<hr />

<h2>💡 Why Not Classify Everything With an LLM?</h2>
<ul>
  <li><b>Cost:</b> LLM calls add up quickly at scale</li>
  <li><b>Latency:</b> Regex/ML is faster</li>
  <li><b>Consistency:</b> Regex/ML outputs are more deterministic</li>
  <li><b>Resilience:</b> Reduces dependency on external API uptime</li>
</ul>

<p>
This project uses an LLM only where it provides the most value: <b>low-data, high-variance logs</b>.
</p>

<hr />
