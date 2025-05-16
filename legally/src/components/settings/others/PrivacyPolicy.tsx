"use client";
import React from "react";

export default function PrivacyPolicy() {
  return (
  <div className="prose prose-blue max-w-4xl mx-auto p-8 bg-white rounded-lg shadow-md">
    <h1>Privacy Policy for Legally</h1>
    <p><strong>Last Updated:</strong> May 2nd, 2025</p>

    <p>
      At <strong>Legally</strong>, your privacy and data security are of paramount importance. This Privacy Policy explains how we collect, use, store, and protect your personal information when you use our services.
    </p>

    <hr />

    <h2>1. Information We Collect</h2>

    <h3>a. User Account Information</h3>
    <ul>
      <li>Name</li>
      <li>Age</li>
      <li>Email address (used for authentication)</li>
      <li>Password (stored securely using hashing)</li>
      <li>User role (e.g., regular user or admin)</li>
    </ul>

    <h3>b. Uploaded Files</h3>
    <ul>
      <li>File name, file path, and unique identifier</li>
      <li>File content (stored securely for processing and retrieval)</li>
      <li>Upload timestamp</li>
    </ul>

    <h3>c. Conversations</h3>
    <ul>
      <li>Your legal questions and our generated responses</li>
      <li>Timestamps of each interaction</li>
      <li>Associated chat session (if any)</li>
    </ul>

    <h3>d. Chat Sessions</h3>
    <ul>
      <li>Session titles</li>
      <li>Creation timestamps</li>
    </ul>

    <h3>e. Technical Information</h3>
    <ul>
      <li>IP address (used for rate limiting and abuse prevention)</li>
      <li>Browser and device metadata (anonymized)</li>
    </ul>

    <hr />

    <h2>2. How We Use Your Information</h2>
    <ul>
      <li>Authenticate and manage your account</li>
      <li>Provide accurate, contextual legal answers</li>
      <li>Organize and retrieve your prior interactions</li>
      <li>Enable file-based legal Q&A</li>
      <li>Improve service performance and reliability</li>
    </ul>

    <hr />

    <h2>3. Data Retention</h2>
    <ul>
      <li>We retain user data as long as the account remains active.</li>
      <li>Uploaded files and conversations are stored until you delete them or your account.</li>
      <li>You may request full data deletion at any time by contacting us.</li>
    </ul>

    <hr />

    <h2>4. Data Security</h2>
    <ul>
      <li>Hashed passwords (bcrypt)</li>
      <li>Encrypted connections (HTTPS)</li>
      <li>Secure file handling and storage</li>
      <li>Role-based access control</li>
      <li>Redis and PostgreSQL with industry-grade practices</li>
    </ul>

    <hr />

    <h2>5. Data Sharing</h2>
    <p>We do not sell or share your personal data with third parties, except:</p>
    <ul>
      <li>When required by law (e.g., legal requests)</li>
      <li>For backend infrastructure (e.g., hosting on Render or database providers)</li>
    </ul>

    <hr />

    <h2>6. Your Rights</h2>
    <ul>
      <li>Access your data</li>
      <li>Correct inaccuracies</li>
      <li>Delete your account and associated data</li>
      <li>Withdraw consent to processing</li>
    </ul>

    <hr />

    <h2>7. Contact</h2>
    <p>
      For questions or requests, either use the contact form or email us at:{" "}
      <a href="mailto:long131005@gmail.com" className="text-blue-600 underline">
        long131005@gmail.com
      </a>
    </p>
  </div>
);
}