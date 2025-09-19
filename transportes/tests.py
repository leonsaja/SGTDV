# transportes/tests.py

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .forms.carro_form import CarroForm
from .models import Carro

class UploadTestCase(TestCase):
    @override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=1024)
    def test_file_size_validation(self):
        # Cria um arquivo que excede o limite de 2 MB do formulário
        file_content = b'x' * (10 * 1024 * 1024)  # 10 MB
        uploaded_file = SimpleUploadedFile(
            "large_file.txt",
            file_content,
            content_type="text/plain"
        )
        
        # O post deve conter os dados obrigatórios do formulário, além do arquivo.
        # Caso contrário, o teste falhará em campos obrigatórios como 'nome' e 'placa'.
        post_data = {
            'nome': 'Carro de Teste',
            'placa': 'ABC-1234',
            'tipo_transporte': '1', # Valor válido de choices
            'cor': 'Preto',
            'ano_fabricacao': 2020,
            'foto': uploaded_file,
        }

        # A URL agora está correta.
        response = self.client.post(reverse('transportes:add-carro'), post_data)
        
        # A view deve retornar o formulário com os erros,
        # portanto o status_code deve ser 200 (OK), não um redirecionamento.
        self.assertEqual(response.status_code, 200)

        # Agora, verifique se o formulário não é válido
        self.assertFalse(response.context['form'].is_valid())
        
        # Verifique se a mensagem de erro esperada está presente
        # A validação de tamanho ocorre no 'clean_foto' do formulário.
        self.assertIn("O arquivo é muito grande.", response.context['form'].errors['foto'][0])