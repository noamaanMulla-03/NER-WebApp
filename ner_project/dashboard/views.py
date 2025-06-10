from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DocumentUploadForm, DocumentSetSelectForm
from .models import DocumentSet, Document
import ollama

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
                title = file.name  # Placeholder: Extract title via PyPDF2/pytesseract
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
            doc_set = DocumentSet.objects.get(id=form.cleaned_data['document_set'], user=request.user)
            titles = [doc.title for doc in doc_set.documents.all()]
            # Call Ollama/DeepSeek-R1
            response = ollama.chat(
                model='deepseek-r1',
                messages=[{'role': 'user', 'content': f'Summarize these document titles: {", ".join(titles)}'}]
            )
            summary = response['message']['content']
            return render(request, 'summary.html', {'form': form, 'document_sets': document_sets, 'summary': summary})
    else:
        form = DocumentSetSelectForm(user=request.user)
    return render(request, 'summary.html', {'form': form, 'document_sets': document_sets})