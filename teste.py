from weasyprint import CSS, HTML

HTML('http://samplewebsite.com/').write_pdf('/home/leonardo/Downloads/test.pdf', stylesheets=[CSS(string='body { font-size: 10px }')])


<div class="row justify-content-center">
      <div class="col-md-4">

        <label for="data_inicial" class="form-label">Data Inicial</label>
        <div class="input-group has-validation">
          <input type="date" name="data_inicial" class="form form-control" id="data_inicial">
         </div>             
         {% if erros.data_inicial %}
            <div class="invalid-feedback">
              {{erros.data}}
            </div>
         {% endif %}
        </div>

      <div class="col-md-4">
        <label for="data_final" class="form-label">Data Final</label>
        <div class="input-group has-validation">

          <input type="date" max="" name="data_final" class="form form-control" id="data_final"
            aria-describedby="inputGroupPrepend" required>
          <div class="invalid-feedback">
            Please choose a username.
          </div>
        </div>
      </div>
    </div>
    <br>
    <div class="row justify-content-center">

      <div class="col-md-8 ml-5">
        <input class="form-check-input" type="checkbox" id="flexCheckChecked">
        <label class="form-check-label" for="flexCheckChecked">
          Checked checkbox
        </label>
      </div>
    </div>