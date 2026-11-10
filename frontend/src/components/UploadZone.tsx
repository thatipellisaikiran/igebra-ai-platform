import React, { useState, useEffect } from 'react';
import { Upload, FileText, CheckCircle2, ArrowRight } from 'lucide-react';
import { api } from '../services/api';

interface UploadZoneProps {
  onContinue: () => void;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onContinue }) => {
  const [uploadedFiles, setUploadedFiles] = useState<any[]>([]);
  const [docType, setDocType] = useState<string>('notes');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    api.listMaterials().then(setUploadedFiles).catch(console.error);
  }, []);

  const handleUpload = async () => {
    if (!selectedFile) return;
    setIsUploading(true);
    try {
      await api.uploadMaterial(selectedFile, docType);
      const updated = await api.listMaterials();
      setUploadedFiles(updated);
      setSelectedFile(null);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8">
        <div className="max-w-2xl">
          <h2 className="text-2xl font-bold text-white tracking-tight">Step 1: Ingest Study Materials</h2>
          <p className="text-slate-400 mt-2 text-sm">
            Upload your syllabus, textbook notes, and past examination papers. The system indexes them with exact section citations for retrieval.
          </p>
        </div>

        <div className="mt-6 border-2 border-dashed border-slate-700 hover:border-indigo-500 rounded-xl p-8 text-center bg-slate-950/40 transition">
          <div className="w-12 h-12 bg-indigo-500/10 text-indigo-400 rounded-xl flex items-center justify-center mx-auto">
            <Upload className="w-6 h-6" />
          </div>
          <h3 className="text-slate-200 font-semibold mt-3 text-sm">Select document type and file</h3>
          <div className="mt-4 flex flex-col sm:flex-row justify-center items-center gap-3">
            <select
              value={docType}
              onChange={(e) => setDocType(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200"
            >
              <option value="syllabus">Syllabus</option>
              <option value="notes">Textbook / Notes</option>
              <option value="past_paper">Past Exam Paper</option>
            </select>
            <input
              type="file"
              accept=".txt,.md,.pdf"
              onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
              className="text-xs text-slate-300"
            />
            <button
              onClick={handleUpload}
              disabled={isUploading || !selectedFile}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-medium transition disabled:opacity-50"
            >
              {isUploading ? 'Parsing & Indexing...' : 'Upload & Index'}
            </button>
          </div>
        </div>

        <div className="mt-8">
          <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
            Active Indexed Documents ({uploadedFiles.length})
          </h3>
          <div className="mt-3 divide-y divide-slate-800 border border-slate-800 rounded-xl overflow-hidden bg-slate-950/50">
            {uploadedFiles.length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-500">No documents uploaded yet.</div>
            ) : (
              uploadedFiles.map((file) => (
                <div key={file.id} className="p-4 flex items-center justify-between hover:bg-slate-800/40 transition">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-slate-800 text-indigo-400 rounded-lg">
                      <FileText className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-slate-200">{file.filename}</h4>
                      <div className="flex items-center space-x-2 text-xs text-slate-400 mt-0.5">
                        <span className="bg-slate-800 px-2 py-0.5 rounded text-[11px] font-medium text-slate-300">
                          {file.doc_type}
                        </span>
                        <span>•</span>
                        <span>{file.chunks_created} semantic chunks</span>
                      </div>
                    </div>
                  </div>
                  <span className="flex items-center text-xs text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full font-medium border border-emerald-500/20">
                    <CheckCircle2 className="w-3.5 h-3.5 mr-1" />
                    Indexed
                  </span>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="mt-8 flex justify-end">
          <button
            onClick={onContinue}
            className="flex items-center space-x-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-medium transition"
          >
            <span>Proceed to Step 2: Topic Map</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
