from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal, InvalidOperation
import math
from .models import Book, Category, Attendance, Classroom, Homework, Student, Score
from django.contrib.auth.decorators import login_required
from .forms import BookForms, ScoreForms, HomeworkForm
from django.contrib import messages

# صفحه اصلی سایت


def home(request):
    return render(request, "home.html")


def physics(request):
    # مقداردهی اولیه متغیر ها
    result = None
    operation = None
    career_vo = None
    career_ar = None
    squre_c = None
    elec = None
    career_ele = None
    heat = None

    # مدیریت خطاها و تبدیل عدد ورودی به دسیمال برای دقت در محاسبه
    def to_decimal(value):
        try:
            return Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return None

    # دریافت اطلاعات ارسال‌شده از فرم که به صورت پست هستند
    if request.method == "POST":
        # به ترتیب آی دی و نوع عملیات
        operation = request.POST.get("operation", "")
        career_vo = request.POST.get("shape", "")
        career_ar = request.POST.get("career_ar", "")
        career_ele = request.POST.get("career_ele", "")
        squre_c = request.POST.get("squre_c", "")
        heat = request.POST.get("heat", "")
        unit = request.POST.get("unit", "")
        unit2 = request.POST.get("unit2", "")

        # عملیات اول چگالی
        if operation == "density":
            # دریافت متغیر ها از فرانت
            ms_d = to_decimal(request.POST.get("mass_d"))
            v_d = to_decimal(request.POST.get("volume_d"))
            # چک کردن متغیر ها
            if ms_d is not None and v_d is not None:
                # انجام عملیات
                rd = ms_d / v_d
                # نشان دادن جواب
                result = f"چگالی: {rd}"
            else:
                # در صورت وارد کردن مقدار نامعتبر
                result = "لطفاً عدد مناسبی برای جرم و حجم وارد کنید."

        elif operation == "volume":
            # انتخاب شکل
            if career_vo == "cube":
                length_cvo = request.POST.get("length_cube")
                len_vo = to_decimal(length_cvo)
                if len_vo is not None:
                    rvo_c = len_vo**3
                    result = f"حجم مکعب: {rvo_c}"
                else:
                    result = "لطفاً عدد مناسبی برای طول و عرض و ارتفاع وارد کنید."

            elif career_vo == "sphere":
                radius_svo = to_decimal(request.POST.get("radius"))
                if radius_svo is not None:
                    rvo_sq = Decimal("4")/Decimal("3") * \
                        Decimal("3.14") * (radius_svo**3)
                    result = f"حجم کره: {rvo_sq}"
                else:
                    result = "لطفاً عدد مناسبی برای شعاع وارد کنید."

            elif career_vo == "rectangularcube":
                h_rvo = to_decimal(request.POST.get("height_rcube"))
                w_rvo = to_decimal(request.POST.get("width_rcube"))
                l_rvo = to_decimal(request.POST.get("length_rcube"))
                if h_rvo is not None and w_rvo is not None and l_rvo is not None:
                    rvo_recc = h_rvo * w_rvo * l_rvo
                    result = f"حجم مکعب مستطیل: {rvo_recc}"
                else:
                    result = "لطفاً عدد مناسبی برای طول و عرض و ارتفاع وارد کنید."

            elif career_vo == "density":
                mass_dvo = to_decimal(request.POST.get("mass_vo"))
                density_dvo = to_decimal(request.POST.get("density_vo"))
                if mass_dvo is not None and density_dvo is not None:
                    rvo_den = mass_dvo / density_dvo
                    result = f"حجم: {rvo_den}"
                else:
                    result = "لطفاً عدد مناسبی برای جرم و چگالی وارد کنید."

        elif operation == "area":
            # به دلیل یکسان بودن فرمول ما این رو در یک لیست آوردیم
            if career_ar in ["مربع", "مستطیل"]:
                lenar = to_decimal(request.POST.get("length_rect"))
                heiar = to_decimal(request.POST.get("height_rect"))
                if lenar is not None and heiar is not None:
                    rar_sqrect = lenar * heiar
                    result = f"مساحت {career_ar}: {rar_sqrect}"
                else:
                    result = "لطفاً عدد مناسبی برای طول و عرض وارد کنید."

            elif career_ar == "triangle":
                bar_tri = to_decimal(request.POST.get("base_tria"))
                h2ar_tri = to_decimal(request.POST.get("height_taria"))
                if bar_tri is not None and h2ar_tri is not None:
                    rar_tri = (bar_tri * h2ar_tri)/2
                    result = f"مساحت مثلث: {rar_tri}"
                else:
                    result = "لطفاً عدد مناسبی برای قاعده و ارتفاع وارد کنید."

            elif career_ar == "rhambus":
                biar_rh = to_decimal(request.POST.get("bigdiameter_rh"))
                siar_dh = to_decimal(request.POST.get("smalldiameter_rh"))
                if biar_rh is not None and siar_dh is not None:
                    rar_rh = (biar_rh * siar_dh)/2
                    result = f"مساحت لوزی: {rar_rh}"
                else:
                    result = "لطفاً عدد مناسبی برای قطر بزرگ و قطر کوچک وارد کنید."

            elif career_ar == "circle":
                if squre_c == "squre_cd":
                    diar_ci = to_decimal(request.POST.get("di_cir"))
                    if diar_ci is not None:
                        rar_cid = (diar_ci/2)**2 * Decimal("3.14")
                        result = f"مساحت دایره: {rar_cid}"
                    else:
                        result = "لطفاً عدد مناسبی برای قطر وارد کنید."
                elif squre_c == "squre_cr":
                    raar_ci = to_decimal(request.POST.get("ra_cir"))
                    if raar_ci is not None:
                        rar_cir = (raar_ci**2) * Decimal("3.14")
                        result = f"مساحت دایره: {rar_cir}"
                    else:
                        result = "لطفاً عدد مناسبی برای شعاع وارد کنید."

            elif career_ar == "cube":
                lear_cu = to_decimal(request.POST.get("length_cu"))
                if lear_cu is not None:
                    rar_cu = (lear_cu**2) * 6
                    result = f"مساحت مکعب: {rar_cu}"
                else:
                    result = "لطفاً عدد مناسبی برای طول وارد کنید."

            elif career_ar == "rc":
                lear_rc = to_decimal(request.POST.get("le_rc"))
                wiar_rc = to_decimal(request.POST.get("wi_rc"))
                hear_rc = to_decimal(request.POST.get("he_rc"))
                if None not in [lear_rc, wiar_rc, hear_rc]:
                    rar_rect = 2*(lear_rc*wiar_rc + lear_rc *
                                  hear_rc + wiar_rc*hear_rc)
                    result = f"مساحت مکعب مستطیل: {rar_rect}"
                else:
                    result = "لطفاً عدد مناسبی برای طول و عرض و ارتفاع وارد کنید."

            elif career_ar == "sphere":
                rar_sq = to_decimal(request.POST.get("ra_sq"))
                if rar_sq is not None:
                    rar_sq = 4 * Decimal("3.14") * (rar_sq**2)
                    result = f"مساحت کره: {rar_sq}"
                else:
                    result = "لطفاً عدد مناسبی برای شعاع وارد کنید."

            elif career_ar == "para":
                baar_para = to_decimal(request.POST.get("ba_para"))
                hear_para = to_decimal(request.POST.get("he_para"))
                if baar_para is not None and hear_para is not None:
                    rar_sq = baar_para * hear_para
                    result = f"مساحت متوازی الاضلاع: {rar_sq}"
                else:
                    result = "لطفاً عدد مناسبی برای قاعده و ارتفاع وارد کنید."

        elif operation == "elec":
            elecs = request.POST.get("career_ele")
            if elecs == "take":
                e_ta = to_decimal(request.POST.get("elec_ta"))
                if e_ta is not None:
                    r_eta = -(e_ta * Decimal("1.6E-19"))
                    result = f"بار الکتریکی: {r_eta}".replace("E", "x10^")
                else:
                    result = "لطفاً عدد مناسبی برای بار الکتریکی گرفته شده را وارد کنید."
            elif elecs == "give":
                e_gi = to_decimal(request.POST.get("elec_gi"))
                if e_gi is not None:
                    r_egi = e_gi * Decimal("1.6E-19")
                    result = f"بار الکتریکی: {r_egi}".replace("E", "x10^")
                else:
                    result = "لطفاً عدد مناسبی برای بارالکتریکی از دست داده شده را وارد کنید."

        elif operation == "coul":
            q1 = to_decimal(request.POST.get("q1_coul"))
            q2 = to_decimal(request.POST.get("q2_coul"))
            d = to_decimal(request.POST.get("dist_coul"))
            if None not in [q1, q2, d] and d != 0:
                # تعریف کردن مقدار ثابت کولون
                K = Decimal("9E9")
                rco = K * q1 * q2 / (d ** 2)
                result = f"نیروی بین دو جسم: {rco}".replace(
                    "E", "x10^")
            else:
                result = "لطفاً عدد مناسبی برای بار الکتریکی و جا به جایی وارد کنید."

        elif operation == "kar":
            f_kar = request.POST.get("force_kar")
            m_kar = request.POST.get("move_kar")
            a_kar = request.POST.get("angle_kar")
            try:
                f1_kar = float(f_kar)
                m1_kar = float(m_kar)
                a1_kar = float(a_kar)
                rad_kar = math.radians(a1_kar)
                if a1_kar == 90.0:
                    rka = 0
                else:
                    rka = f1_kar * m1_kar * (math.cos(rad_kar))
                result = f"کار: {rka}"
            except:
                result = "لطفاً عدد مناسبی برای نیرو و جا به جایی و زاوین بین آن دو وارد کنید."

        elif operation == "hot":
            heat = request.POST.get("heat")
            if heat == "c":
                cho = request.POST.get("spe_heat")
                mho = request.POST.get("mas_heat")
                spo = request.POST.get("spe_heat")
                try:
                    c1ho = float(cho)
                    m1ho = float(mho)
                    spo1ho = float(spo)
                    rhe = c1ho * m1ho * spo1ho
                    result = f"گرما: {rhe}"
                except:
                    result = "لطفاً عدد مناسبی برای گرمای ویژه و جرم و دما وارد کنید."
            elif heat == "C":
                ca_he = request.POST.get("cap_heat")
                ste_he = request.POST.get("stemp_heat")
                try:
                    ca1_he = float(ca_he)
                    ste2_he = float(ste_he)
                    rhe = ca1_he * ste2_he
                    result = f"گرما: {rhe}"
                except:
                    result = "لطفاً عدد مناسبی برای گرما و دما وارد کنید."

        elif operation == "unit":
            value = to_decimal(request.POST.get("value"))
            unit1 = request.POST.get("unit")
            unit2 = request.POST.get("unit2")

            prefixes = {
                "deca": 1e1, "hecto": 1e2, "kilo": 1e3, "mega": 1e6, "giga": 1e9, "tra": 1e12,
                "deci": 1e-1, "centi": 1e-2, "mili": 1e-3, "micro": 1e-6, "nano": 1e-9, "pico": 1e-12
            }

            if value is not None and unit1 in prefixes and unit2 in prefixes:
                base_value = value * Decimal(prefixes[unit1])
                result_value = base_value / Decimal(prefixes[unit2])

                # نمایش عدد به صورت علمی یعنی با دو رقم اعشار
                scientific = f"{result_value:.2E}"
                # حذف E از جواب
                mantissa, exponent = scientific.split("E")
                # تبدیل توان به عدد
                exp = int(exponent)
                # جدولی که عدد هارا با توانشون جا به جا میکنه
                superscript_map = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")
                # جا به جا کردن توان و عدد
                exp_sup = str(exp).translate(superscript_map)
                formatted = f"{mantissa} × 10{exp_sup}"

                result = f"Converted value: {formatted}"
            else:
                result = "لطفاً عدد مناسبی برای مقدار وارد کنید."

    return render(request, "physics.html", {
        "result": result,
        "operation": operation,
        "career_vo": career_vo,
        "career_ar": career_ar,
        "squre_c": squre_c,
        "elec": elec,
        "career_ele": career_ele,
        "heat": heat,
    })


def math_calc(request):
    result = None
    operation = None
    career_sin = None
    career_cos = None

    def to_decimal(value):
        try:
            return Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return None

    if request.method == "POST":
        operation = request.POST.get("operation", "")
        career_cos = request.POST.get("career_cos", "")
        career_sin = request.POST.get("career_sin", "")
        if operation == "calc_side3":
            s_1 = to_decimal(request.POST.get("side1"))
            s_2 = to_decimal(request.POST.get("side2"))
            ang_bet = to_decimal(request.POST.get("angle_bet"))

            if s_1 is not None and s_2 is not None and ang_bet is not None:
                ang_bet_rad = math.radians(ang_bet)
                r_calcs32 = (s_1 ** 2) + (s_2 ** 2) - (2 * s_1 *
                                                       s_2 * to_decimal(math.cos(ang_bet_rad)))
                # رادیکال گرفتن
                r_calcs3 = math.sqrt(r_calcs32)
                result = f"ضلع سوم: {r_calcs3}"
            else:
                result = "لطفاً عدد مناسبی برای ضلع و زاویه بین وارد کنید."
        elif operation == "pythagoras":
            rs_1 = to_decimal(request.POST.get("r_side1"))
            rs_2 = to_decimal(request.POST.get("r_side2"))

            if rs_1 is not None and rs_2 is not None:
                rs_ch = math.sqrt((rs_1 ** 2) + (rs_2 ** 2))
                result = f"وتر: {rs_ch}"
            else:
                result = "لطفاً عدد مناسبی برای ضلع وارد کنید."
        elif operation == "sinus":
            career_sin = request.POST.get("career_sin")
            if career_sin == "w_angle":
                angle_b = to_decimal(request.POST.get("angle_w"))
                if angle_b is not None:
                    # تبدیل به رادیان
                    ang_bet = math.radians(angle_b)
                    r_calcsin = math.sin(ang_bet)
                    result = f"سینوس: {r_calcsin}"
                else:
                    result = "لطفاً عدد مناسبی برای زاویه وارد کنید."
            elif career_sin == "w_formula":
                ang_acr = to_decimal(request.POST.get("angle_acr"))
                s_ch = to_decimal(request.POST.get("s_chord"))
                if ang_acr is not None and s_ch is not None:
                    rs_calcsin = ang_acr / s_ch
                    result = f"سینوس: {rs_calcsin}"
                else:
                    result = "لطفاً عدد مناسبی برای ضلع مقابل و وتر وارد کنید."
        elif operation == "cosinus":
            career_cos = request.POST.get("career_cos")
            if career_cos == "w_angle":
                angle_b = to_decimal(request.POST.get("angle_w"))
                if angle_b is not None:
                    ang_bet = math.radians(angle_b)
                    r_calccos = math.cos(ang_bet)
                    result = f"کسینوس: {r_calccos}"
                else:
                    result = "لطفاً عدد مناسبی برای زاویه وارد کنید."
            elif career_cos == "w_formula":
                ang_adj = to_decimal(request.POST.get("angle_adj"))
                s_ch = to_decimal(request.POST.get("s-chord"))
                if ang_adj is not None and s_ch is not None:
                    rs_calccos = ang_adj / s_ch
                    result = f"کسینوس: {rs_calccos}"
                else:
                    result = "لطفاً عدد مناسبی برای ضلع مجاور و وتر وارد کنید."
        elif operation == "inscribed_ang":
            cir_bow = to_decimal(request.POST.get("bow_angle"))

            if cir_bow is not None:
                rs_ins = cir_bow / 2
                result = f"زاویه محاطی: {rs_ins}"
            else:
                result = "Please enter valid numbers for bow."
    return render(request, "math.html", {
        "operation": operation,
        "result": result,
        "career_sin": career_sin,
        "career_cos": career_cos
    })


@login_required
def appear_book(request):
    # پردازش فرم آپلود
    if request.method == 'POST':
        # ایجاد فرم با اطلاعات و فایل‌های ارسالی
        form = BookForms(request.POST, request.FILES)
        # چک کردن فایل
        if form.is_valid():
            # سیو کردن فایل
            form.save()
            # نمایش پیام
            messages.success(
                request, 'جزوه شما با موفقیت ارسال شد و پس از بررسی ادمین نمایش داده می‌شود.')
            return redirect('main:show_book')
    else:
        form = BookForms()

    # فقط موارد تأیید شده
    resources = Book.objects.filter(
        status=Book.StatusChoices.APPROVED).select_related('category')
    # دریافت تمام دسته‌بندی‌ها
    categories = Category.objects.all()

    # فیلتر جستجو
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', 'all')

    # فیلتر فایل ها بر اساس عنوان
    if query:
        resources = resources.filter(title__icontains=query)

    if category_slug != 'all':
        resources = resources.filter(category__slug=category_slug)

    context = {
        'resources': resources,
        'categories': categories,
        'form': form,
        'current_query': query,
        'current_category': category_slug
    }
    return render(request, 'appear_book.html', context)


def help(request):
    return render(request, 'help.html')


def book_detail(request, id):
    book = get_object_or_404(Book, id=id, status=Book.StatusChoices.APPROVED)
    context = {"book": book}
    return render(request, "book_detail.html", context)


def dashboard(request):
    student = None

    if hasattr(request.user, "profile") and request.user.profile.role == "student":
        student = Student.objects.get(user=request.user)

    return render(request, "dashboard.html", {
        "student": student
    })


def stu_list(request):
    classrooms = Classroom.objects.all()
    return render(request, 'stu_list.html', {"classrooms": classrooms})


def homework(request):
    homeworks = Homework.objects.all()
    return render(request, 'homework.html', {"homeworks": homeworks})


def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    homeworks = Homework.objects.filter(classroom=student.classroom)
    scores = Score.objects.filter(student=student, status="approved")
    attendances = Attendance.objects.filter(student=student).order_by("-date", "-time")
    return render(request, "student_detail.html", {
        "student": student,
        "homeworks": homeworks,
        "scores": scores,
        "attendances": attendances,
    })


def add_grade(request):
    if request.method == "POST":
        form = ScoreForms(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")

    form = ScoreForms()
    return render(request, "add_grade.html", {"form": form})


def attendance_page(request, classroom_id):
    classroom = get_object_or_404(
        Classroom,
        id=classroom_id
    )

    students = Student.objects.filter(
        classroom=classroom
    )

    if request.method == "POST":

        for student in students:

            status = request.POST.get(
                f"student_{student.id}"
            )

            Attendance.objects.create(student=student,classroom=classroom,status=status)
        return redirect("main:attendance", classroom_id=classroom_id)
    context = {
        "classroom": classroom,
        "students": students
    }

    return render(request,"attendance.html",context)

@login_required
def student_dashboard(request):
    student = get_object_or_404(Student,user=request.user)
    scores = Score.objects.filter(student=student,status="approved")
    attendances = Attendance.objects.filter(student=student).order_by("-date")
    homeworks = Homework.objects.filter(classroom=student.classroom).order_by("-id")
    context = {
        "student": student,
        "scores": scores,
        "attendances": attendances,
        "homeworks": homeworks,
    }
    return render(request, "student_dashboard.html", context)

def add_homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تکلیف با موفقیت بارگزاری شد")
    else:
        form = HomeworkForm()
    return render(request,"add_homework.html",{"form": form})