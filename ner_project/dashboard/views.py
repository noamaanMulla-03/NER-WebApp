from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DocumentUploadForm, DocumentSetSelectForm
from .models import DocumentSet, Document
import ollama
import re

def markdown_to_html(text):
    return re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', text)


@login_required
def upload_view(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc_set = DocumentSet.objects.create(
                name=form.cleaned_data['set_name'],
                user=request.user
            )
            for file in request.FILES.getlist('documents'):
                title = file.name
                Document.objects.create(
                    document_set=doc_set,
                    file=file,
                    title=title
                )
            messages.success(request, 'Documents uploaded successfully.')
            return redirect('upload')
        else:
            messages.error(request, 'Upload failed. Please correct the errors.')
    else:
        form = DocumentUploadForm()
    return render(request, 'upload.html', {'form': form})


@login_required
def summary_view(request):
    document_sets = DocumentSet.objects.filter(user=request.user)
    if request.method == 'POST':
        form = DocumentSetSelectForm(request.POST, user=request.user)
        if form.is_valid():
            doc_set = form.cleaned_data['document_set']
            titles = [doc.title for doc in doc_set.documents.all()]
            prompt = (
                f"Generate concise, professional summaries for the following document titles, "
                f"each as a separate paragraph starting with the title in bold (e.g., **Title.pdf**), "
                f"followed by a colon and the summary (1-2 sentences describing content and purpose in a technical or academic context). "
                f"Return ONLY the summaries in this format, without numbering, reasoning, `<think>` tags, or any other text. "
                f"Example:\n**Title1.pdf**: Description.\n\n**Title2.pdf**: Description.\nTitles: {', '.join(titles)}"
            )

            try:
                response = ollama.chat(
                    model='qwen2:0.5b',
                    messages=[{'role': 'user', 'content': prompt}]
                )
                summary = response['message']['content']
                summary_lines = summary.splitlines()
                valid_lines = []

                for line in summary_lines:
                    if re.match(r'^\*\*[^\*]+\*\*:\s*', line.strip()):
                        valid_lines.append(line.strip().rstrip()) 
                summary = '\n\n'.join([f'<p>{line}</p><br>' for line in valid_lines]) if valid_lines else "No valid summaries generated."
                summary = markdown_to_html(summary)
            except Exception as e:
                summary = "Error generating summary."
                messages.error(request, f"LLM error: {str(e)}")
            
            return render(request, 'summary.html', {'form': form, 'document_sets': document_sets, 'summary': summary})
    else:
        form = DocumentSetSelectForm(user=request.user)
    return render(request, 'summary.html', {'form': form, 'document_sets': document_sets})