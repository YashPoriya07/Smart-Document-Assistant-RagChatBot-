'use client';

import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          {/* Hero Section */}
          <div className="mb-12">
            <h1 className="text-6xl font-bold text-white mb-6">
              AI Document Chatbot
            </h1>
            <p className="text-xl text-blue-100 mb-8">
              Upload your PDF documents and chat with an AI that understands them.
              Get instant answers backed by your content.
            </p>
            <Link
              href="/upload"
              className="inline-block bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-50 transition shadow-2xl hover:shadow-3xl transform hover:scale-105"
            >
              Get Started
            </Link>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-8 mt-20">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <div className="bg-white/20 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                <svg
                  className="h-8 w-8 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                Easy Upload
              </h3>
              <p className="text-blue-100">
                Drag and drop up to 15 PDF files. Simple, fast, and secure.
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <div className="bg-white/20 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                <svg
                  className="h-8 w-8 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                Smart AI
              </h3>
              <p className="text-blue-100">
                Powered by advanced RAG technology for accurate, context-aware responses.
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <div className="bg-white/20 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                <svg
                  className="h-8 w-8 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                Source Citations
              </h3>
              <p className="text-blue-100">
                Every answer includes references to the original documents.
              </p>
            </div>
          </div>

          {/* How It Works */}
          <div className="mt-20">
            <h2 className="text-3xl font-bold text-white mb-12">
              How It Works
            </h2>
            <div className="space-y-6">
              <div className="flex items-start text-left bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <div className="bg-blue-500 text-white rounded-full h-10 w-10 flex items-center justify-center font-bold flex-shrink-0 mr-4">
                  1
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-white mb-2">
                    Upload Your Documents
                  </h4>
                  <p className="text-blue-100">
                    Select and upload your PDF files. Our system supports up to 15 files at once.
                  </p>
                </div>
              </div>

              <div className="flex items-start text-left bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <div className="bg-purple-500 text-white rounded-full h-10 w-10 flex items-center justify-center font-bold flex-shrink-0 mr-4">
                  2
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-white mb-2">
                    AI Processing
                  </h4>
                  <p className="text-blue-100">
                    Our AI reads and understands your documents, creating a knowledge base.
                  </p>
                </div>
              </div>

              <div className="flex items-start text-left bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <div className="bg-indigo-500 text-white rounded-full h-10 w-10 flex items-center justify-center font-bold flex-shrink-0 mr-4">
                  3
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-white mb-2">
                    Start Chatting
                  </h4>
                  <p className="text-blue-100">
                    Ask questions and get accurate answers with source citations.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* CTA */}
          <div className="mt-20">
            <Link
              href="/upload"
              className="inline-block bg-white text-blue-600 px-10 py-5 rounded-xl font-bold text-xl hover:bg-blue-50 transition shadow-2xl hover:shadow-3xl transform hover:scale-105"
            >
              Upload Documents Now →
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
