$(document).ready(function () {
    const host = "api/v1"

    function requestCurrencies() {
        $.ajax({
            url: `${host}/currencies/`,
            type: "GET",
            dataType: "json",
            success: function (data) {
                const tbody = $('.currencies-table tbody');
                tbody.empty();
                $.each(data, function (index, currency) {
                    const row = $('<tr></tr>');
                    row.append($('<td></td>').text(currency.code));
                    row.append($('<td></td>').text(currency.fullname));
                    row.append($('<td></td>').text(currency.sign));
                    tbody.append(row);
                });

                const newRateBaseCurrency = $("#new-rate-base-currency");
                newRateBaseCurrency.empty();

                $.each(data, function (index, currency) {
                    newRateBaseCurrency.append(`<option value="${currency.code}">${currency.code}</option>`);
                });

                const newRateTargetCurrency = $("#new-rate-target-currency");
                newRateTargetCurrency.empty();

                $.each(data, function (index, currency) {
                    newRateTargetCurrency.append(`<option value="${currency.code}">${currency.code}</option>`);
                });

                const convertBaseCurrency = $("#convert-base-currency");
                convertBaseCurrency.empty();

                $.each(data, function (index, currency) {
                    convertBaseCurrency.append(`<option value="${currency.code}">${currency.code}</option>`);
                });

                const convertTargetCurrency = $("#convert-target-currency");
                convertTargetCurrency.empty();

                $.each(data, function (index, currency) {
                    convertTargetCurrency.append(`<option value="${currency.code}">${currency.code}</option>`);
                });
            },
            error: function (jqXHR, textStatus, errorThrown) {
                const error = JSON.parse(jqXHR.responseText);
                const toast = $('#api-error-toast');

                let errorMessage = '';
                for (const [key, value] of Object.entries(error)) {
                    errorMessage += `<b>${key}</b>: ${value}<br>`; // Используем <br> для переноса строк
                }
                $(toast).find('.toast-body').html(errorMessage);
                toast.toast("show");
            }
        });
    }

    requestCurrencies();

    $("#add-currency").submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: `${host}/currencies/`,
            type: "POST",
            data: $("#add-currency").serialize(),
            success: function (data) {
                requestCurrencies();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                const error = JSON.parse(jqXHR.responseText);
                const toast = $('#api-error-toast');

                let errorMessage = '';
                for (const [key, value] of Object.entries(error)) {
                    errorMessage += `<b>${key}</b>: ${value}<br>`; // Используем <br> для переноса строк
                }
                $(toast).find('.toast-body').html(errorMessage);
                toast.toast("show");
            }
        });

        return false;
    });

    function requestExchangeRates() {
        $.ajax({
            url: `${host}/exchangeRates/`,
            type: "GET",
            dataType: "json",
            success: function (response) {
                const tbody = $('.exchange-rates-table tbody');
                tbody.empty();
                $.each(response, function (index, rate) {
                    const row = $('<tr></tr>');
                    const currency = rate.base_currency.code + rate.target_currency.code;
                    const exchangeRate = rate.rate;
                    row.append($('<td></td>').text(currency));
                    row.append($('<td></td>').text(exchangeRate));
                    row.append($('<td></td>').html(
                        '<button class="btn btn-secondary btn-sm exchange-rate-edit"' +
                        'data-bs-toggle="modal" data-bs-target="#edit-exchange-rate-modal">Edit</button>'
                    ));
                    tbody.append(row);
                });
            },
            error: function () {
                const error = JSON.parse(jqXHR.responseText);
                const toast = $('#api-error-toast');

                let errorMessage = '';
                for (const [key, value] of Object.entries(error)) {
                    errorMessage += `<b>${key}</b>: ${value}<br>`; // Используем <br> для переноса строк
                }
                $(toast).find('.toast-body').html(errorMessage);
                toast.toast("show");
            }
        });
    }

    requestExchangeRates();

    $(document).delegate('.exchange-rate-edit', 'click', function () {
        const pair = $(this).closest('tr').find('td:first').text();
        const exchangeRate = $(this).closest('tr').find('td:eq(1)').text();

        $('#edit-exchange-rate-modal .modal-title').text(`Edit ${pair} Exchange Rate`);
        $('#edit-exchange-rate-modal #exchange-rate-input').val(exchangeRate);
    });

    $('#edit-exchange-rate-modal .btn-primary').click(function () {
        const pair = $('#edit-exchange-rate-modal .modal-title').text().replace('Edit ', '').replace(' Exchange Rate', '');
        const exchangeRate = $('#edit-exchange-rate-modal #exchange-rate-input').val();

        const row = $(`tr:contains(${pair})`);
        row.find('td:eq(1)').text(exchangeRate);

        $.ajax({
            url: `${host}/exchangeRate/${pair}/`,
            type: "PATCH",
            contentType: "application/x-www-form-urlencoded",
            data: `rate=${exchangeRate}`,
            success: function () {

            },
            error: function (jqXHR, textStatus, errorThrown) {
                const error = JSON.parse(jqXHR.responseText);
                const toast = $('#api-error-toast');

                let errorMessage = '';
                for (const [key, value] of Object.entries(error)) {
                    errorMessage += `<b>${key}</b>: ${value}<br>`; // Используем <br> для переноса строк
                }
                $(toast).find('.toast-body').html(errorMessage);
                toast.toast("show");
            }
        });

        $('#edit-exchange-rate-modal').modal('hide');
    });

    $("#add-exchange-rate").submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: `${host}/exchangeRates/`,
            type: "POST",
            data: $("#add-exchange-rate").serialize(),
            success: function (data) {
                requestExchangeRates();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                const error = JSON.parse(jqXHR.responseText);
                const toast = $('#api-error-toast');

                let errorMessage = '';
                for (const [key, value] of Object.entries(error)) {
                    errorMessage += `<b>${key}</b>: ${value}<br>`; // Используем <br> для переноса строк
                }
                $(toast).find('.toast-body').html(errorMessage);
                toast.toast("show");
            }
        });

        return false;
    });

    $("#convert").submit(function (e) {
        e.preventDefault();

        const baseCurrency = $("#convert-base-currency").val();
        const targetCurrency = $("#convert-target-currency").val();
        const amount = $("#convert-amount").val();

        $.ajax({
            url: `${host}/exchange?base=${baseCurrency}&target=${targetCurrency}&amount=${amount}`,
            type: "GET",
            success: function (data) {
                $("#convert-converted-amount").val(data.convertedAmount);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                const error = JSON.parse(jqXHR.responseText);
                const toast = $('#api-error-toast');

                let errorMessage = '';
                for (const [key, value] of Object.entries(error)) {
                    errorMessage += `<b>${key}</b>: ${value}<br>`; // Используем <br> для переноса строк
                }
                $(toast).find('.toast-body').html(errorMessage);
                toast.toast("show");
            }
        });

        return false;
    });
});
