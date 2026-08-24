import 'package:flutter/services.dart';

class CpfCnpjFormatter extends TextInputFormatter {
  @override
  TextEditingValue formatEditUpdate(
    TextEditingValue oldValue,
    TextEditingValue newValue,
  ) {
    String text = newValue.text.replaceAll(RegExp(r'[^\d]'), '');

    if (text.length > 14) {
      text = text.substring(0, 14);
    }

    String formatted = '';
    if (text.length <= 11) {
      // CPF: 000.000.000-00
      for (int i = 0; i < text.length; i++) {
        if (i == 3 || i == 6) formatted += '.';
        if (i == 9) formatted += '-';
        formatted += text[i];
      }
    } else {
      // CNPJ: 00.000.000/0000-00
      for (int i = 0; i < text.length; i++) {
        if (i == 2 || i == 5) formatted += '.';
        if (i == 8) formatted += '/';
        if (i == 12) formatted += '-';
        formatted += text[i];
      }
    }

    return TextEditingValue(
      text: formatted,
      selection: TextSelection.collapsed(offset: formatted.length),
    );
  }
}
