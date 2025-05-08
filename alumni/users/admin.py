import io
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from openpyxl import Workbook
from .models import CustomUser, ValidRegisterNumber
from openpyxl.styles import Font


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'user_type', 'bio', 'profile_picture',
                'register_number', 'department', 'academic_year',
                'phone_number', 'address',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'classes': ('wide',),
            'fields': (
                'user_type', 'bio', 'profile_picture',
                'register_number', 'department', 'academic_year',
                'phone_number', 'address',
            ),
        }),
    )

    list_display = (
        'username', 'email', 'department', 'phone_number',
        'user_type', 'register_number', 'academic_year', 'address',
    )

    search_fields = (
        'username', 'email',
        'register_number', 'phone_number', 'address'
    )

    list_filter = ('user_type', 'department', 'academic_year')

    actions = ['export_selected_users_pdf', 'export_selected_users_excel']

    def export_selected_users_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=20, leftMargin=20,
            topMargin=20, bottomMargin=20
        )

        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("User Details", styles['Title']))
        elements.append(Spacer(1, 12))

        # Table headers
        data = [[
            'Username', 'Email', 'User Type', 'Register Number',
            'Department', 'Academic Year', 'Phone Number', 'Address'
        ]]

        # Table rows with text wrapping
        for user in queryset:
            data.append([
                Paragraph(user.username or '', styles['Normal']),
                Paragraph(user.email or '', styles['Normal']),
                Paragraph(user.user_type or '', styles['Normal']),
                Paragraph(user.register_number or '', styles['Normal']),
                Paragraph(user.department or '', styles['Normal']),
                Paragraph(str(user.academic_year) or '', styles['Normal']),
                Paragraph(user.phone_number or '', styles['Normal']),
                Paragraph(user.address or '', styles['Normal']),
            ])

        table = Table(data, repeatRows=1)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)
        doc.build(elements)
        buffer.seek(0)

        return HttpResponse(buffer, content_type='application/pdf', headers={
            'Content-Disposition': 'attachment; filename="user_details.pdf"'
        })

    export_selected_users_pdf.short_description = "Export selected users to PDF"

    def export_selected_users_excel(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.title = "User Details"
        
        # Bold header font
        bold_font = Font(bold=True)

        # header
        headers = [
            'Username', 'Email', 'User Type', 'Register Number',
            'Department', 'Academic Year', 'Phone Number', 'Address'
        ]
        ws.append(headers)

        # Apply bold font to header row
        for col in range(1, len(headers) + 1):
            ws.cell(row=1, column=col).font = bold_font

        for user in queryset:
            ws.append([
                user.username,
                user.email,
                user.user_type,
                user.register_number,
                user.department,
                user.academic_year,
                user.phone_number,
                user.address,
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="user_details.xlsx"'
        wb.save(response)
        return response

    export_selected_users_excel.short_description = "Export selected users to Excel"


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(ValidRegisterNumber)


# user/admin.py
from django.contrib import admin
from django import forms
from .models import ValidRegisterNumber
import re

class RegisterNumberRangeForm(forms.ModelForm):
    range_input = forms.CharField(
        label="Register Number Range (e.g., 23MCA01-23MCA30)",
        help_text="Enter a single register number or a range like 23MCA01-23MCA30",
        required=True
    )

    class Meta:
        model = ValidRegisterNumber
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        range_input = cleaned_data.get("range_input")

        if not range_input:
            raise forms.ValidationError("Please provide a register number or range.")

        # Match range like 23MCA01-23MCA30 or single like 23MCA01
        pattern = r'^([A-Za-z0-9]+?)(\d+)(?:-([A-Za-z0-9]+?)(\d+))?$'
        match = re.match(pattern, range_input)

        if not match:
            raise forms.ValidationError("Invalid format. Use like 23MCA01 or 23MCA01-23MCA30")

        prefix1, start_num, prefix2, end_num = match.groups()

        if prefix2 and prefix1 != prefix2:
            raise forms.ValidationError("Prefixes must match in a range.")

        cleaned_data['prefix'] = prefix1
        cleaned_data['start'] = int(start_num)
        cleaned_data['end'] = int(end_num) if end_num else int(start_num)
        cleaned_data['width'] = len(start_num)

        return cleaned_data

class ValidRegisterNumberAdmin(admin.ModelAdmin):
    form = RegisterNumberRangeForm

    def save_model(self, request, obj, form, change):
        prefix = form.cleaned_data['prefix']
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        width = form.cleaned_data['width']

        created = 0
        for i in range(start, end + 1):
            register_number = f"{prefix}{str(i).zfill(width)}"
            _, created_flag = ValidRegisterNumber.objects.get_or_create(register_number=register_number)
            if created_flag:
                created += 1

        self.message_user(request, f"{created} register number(s) added successfully.")

    def has_add_permission(self, request):
        return True

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj=None, **kwargs)

admin.site.register(ValidRegisterNumber, ValidRegisterNumberAdmin)
