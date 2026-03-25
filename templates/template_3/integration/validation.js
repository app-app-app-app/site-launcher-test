const forms = document.querySelectorAll('.leadform');
const errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];
const languagesByCountry = {
    'AL': 'sq', 'AD': 'ca', 'AM': 'hy', 'AT': 'de', 'AZ': 'az', 'BY': 'be', 'BE': 'nl', 'BA': 'bs', 'BG': 'bg',
    'HR': 'hr', 'CY': 'el', 'CZ': 'cs', 'DK': 'da', 'EE': 'et', 'FI': 'fi', 'FR': 'fr', 'GE': 'ka', 'DE': 'de',
    'GR': 'el', 'HU': 'hu', 'IS': 'is', 'IE': 'ga', 'IT': 'it', 'KZ': 'kk', 'LV': 'lv', 'LI': 'de', 'LT': 'lt',
    'LU': 'lb', 'MT': 'mt', 'MD': 'ro', 'MC': 'fr', 'ME': 'sr', 'NL': 'nl', 'MK': 'mk', 'NO': 'no', 'PL': 'pl',
    'PT': 'pt', 'RO': 'ro', 'SM': 'it', 'RS': 'sr', 'SK': 'sk', 'SI': 'sl', 'ES': 'es', 'SE': 'sv', 'CH': 'de',
    'TR': 'tr', 'GB': 'en', 'VA': 'it', 'CA': 'en', 'AU': 'en'
};

const disposableEmailDomains = [
    '10minutemail.com',
    '10minutemail.net',
    '20minutemail.com',
    'dispostable.com',
    'guerrillamail.com',
    'guerrillamailblock.com',
    'grr.la',
    'sharklasers.com',
    'mailinator.com',
    'maildrop.cc',
    'tempmail.com',
    'temp-mail.org',
    'throwawaymail.com',
    'yopmail.com',
    'getnada.com',
    'fakeinbox.com',
    'trashmail.com',
    'mintemail.com',
    'emailondeck.com',
    'moakt.com',
    'zebyinbox.com',
    'ourtimesupport.com',
    'moneysquad.org',
    'orimi.co',
    'usaaxa.com',
    'bdcimail.com',
    'aol.com',
    'webmai.co',
    'gmxxail.com',
    'fxzig.com',
    'talktalk.net',
    'denipl.com',
    'tf-info.com',
    'btinternet.com',
    'ourtimesupport.com',
    'approject.net',
    'banlamail.com',
    'dpvmx.com',
    'wls1.com',
    'mailrez.com',
    'bocah.team',
    'mrotzis.com',
];

function getLanguageByGeo(geo) {
    return languagesByCountry[geo] || 'uk';
}

async function getCountryByIP() {
    try {
        const response = await fetch('https://ipapi.co/json/');
        const data = await response.json();
        return data.country;
    } catch (error) {
        console.error('Error while retrieving country data:', error);
        return 'UA';
    }
}

function isOnlyCountries(form, onlyCountries, itiCountry) {
    if (onlyCountries.length > 0) {
        if (!onlyCountries.includes(itiCountry)) {
            showError(form, "This country is not supported");
            return true;
        }
    }

    return false;
}

function showError(form, msg) {
    const errorMsg = form.querySelector('.error-msg');
    if (!errorMsg) return;

    errorMsg.innerHTML = msg;
    errorMsg.classList.remove("hide");
}

function reset(form) {
    const phone = form.querySelector('input[name="fullphone"]');
    const email = form.querySelector('input[name="email"]');
    const errorMsg = form.querySelector('.error-msg');

    if (phone) {
        phone.classList.remove("error");
    }

    if (email) {
        email.classList.remove("error");
    }

    if (errorMsg) {
        errorMsg.innerHTML = "";
        errorMsg.classList.add("hide");
    }
}

function showPhoneError(form, msg) {
    const phone = form.querySelector('input[name="fullphone"]');
    if (phone) {
        phone.classList.add("error");
    }
    showError(form, msg);
}

function showEmailError(form, msg) {
    const email = form.querySelector('input[name="email"]');
    if (email) {
        email.classList.add("error");
    }
    showError(form, msg);
}

function normalizeEmail(email) {
    return email.trim();
}

function isDisposableEmailDomain(domain) {
    const normalizedDomain = domain.toLowerCase();

    return disposableEmailDomains.some(disposableDomain => {
        return normalizedDomain === disposableDomain || normalizedDomain.endsWith('.' + disposableDomain);
    });
}

function validateEmail(email) {
    const value = normalizeEmail(email);

    if (!value) {
        return { valid: false, message: "Required" };
    }

    if (/\s/.test(value)) {
        return { valid: false, message: "Email must not contain spaces" };
    }

    const atCount = (value.match(/@/g) || []).length;
    if (atCount !== 1) {
        return { valid: false, message: "Invalid email address" };
    }

    const parts = value.split('@');
    const localPart = parts[0];
    const domain = parts[1];

    if (!localPart || !domain) {
        return { valid: false, message: "Invalid email address" };
    }


    if (value.length > 254) {
        return { valid: false, message: "Email is too long" };
    }

    if (localPart.length > 64) {
        return { valid: false, message: "Email name is too long" };
    }

    if (domain.length > 255) {
        return { valid: false, message: "Domain is too long" };
    }

    if (value.includes('..')) {
        return { valid: false, message: "Email must not contain consecutive dots" };
    }

    const localRegex = /^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$/;
    if (!localRegex.test(localPart)) {
        return { valid: false, message: "Invalid characters in email" };
    }

    if (localPart.startsWith('.') || localPart.endsWith('.')) {
        return { valid: false, message: "Invalid email address" };
    }

    if (!domain.includes('.')) {
        return { valid: false, message: "Domain must contain a dot" };
    }

    const domainParts = domain.split('.');

    for (const part of domainParts) {
        if (!part) {
            return { valid: false, message: "Invalid domain" };
        }

        if (part.length > 63) {
            return { valid: false, message: "Domain label is too long" };
        }

        if (part.startsWith('-') || part.endsWith('-')) {
            return { valid: false, message: "Invalid domain" };
        }

        if (!/^[A-Za-z0-9-]+$/.test(part)) {
            return { valid: false, message: "Invalid domain characters" };
        }
    }

    const tld = domainParts[domainParts.length - 1];
    if (tld.length < 2) {
        return { valid: false, message: "Invalid top-level domain" };
    }

    if (isDisposableEmailDomain(domain)) {
        return { valid: false, message: "Disposable email addresses are not allowed" };
    }

    return { valid: true, message: "" };
}

function setupFormValidation(form) {
    const phone = form.querySelector('input[name="fullphone"]');
    const email = form.querySelector('input[name="email"]');
    const country = form.querySelector('input[name="country"]');
    const language = form.querySelector('input[name="language"]');
    const only_countries = form.querySelector('input[name="only_countries"]');
    const phone_country = form.querySelector('input[name="phone_country"]');
    const preloader = form.querySelector('.form-preloader');

    if (!phone || !country || !language || !only_countries || !phone_country || !preloader) {
        return;
    }

    let only_countries_value = [];
    try {
        only_countries_value = JSON.parse(only_countries.value || '[]');
    } catch (e) {
        console.error('Invalid only_countries JSON:', e);
        only_countries_value = [];
    }

    const iti = window.intlTelInput(phone, {
        utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/js/utils.js",
        separateDialCode: true,
        initialCountry: phone_country.value,
        onlyCountries: only_countries_value,
        geoIpLookup: function (success, failure) {
            fetch("https://ipapi.co/json")
                .then(function (res) { return res.json(); })
                .then(function (data) { success(data.country_code); })
                .catch(function () { failure(); });
        }
    });

    phone.addEventListener('blur', function () {
        reset(form);

        if (!phone.value.trim()) {
            showPhoneError(form, "Required");
        } else if (!iti.isValidNumber()) {
            const errorCode = iti.getValidationError();
            const msg = errorMap[errorCode] || "Invalid number";
            showPhoneError(form, msg);
        }
    });

    if (email) {
        email.addEventListener('blur', function () {
            reset(form);

            const result = validateEmail(email.value);
            if (!result.valid) {
                showEmailError(form, result.message);
            } else {
                email.value = normalizeEmail(email.value);
            }
        });

        email.addEventListener('input', function () {
            if (email.classList.contains('error')) {
                reset(form);
            }
        });
    }


    phone.addEventListener('input', function () {
        if (phone.classList.contains('error')) {
            reset(form);
        }
    });

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        reset(form);

        if (email) {
            const emailResult = validateEmail(email.value);
            if (!emailResult.valid) {
                showEmailError(form, emailResult.message);
                return;
            }
            email.value = normalizeEmail(email.value);
        }

        if (!phone.value.trim()) {
            showPhoneError(form, "Required");
            return;
        }

        if (!iti.isValidNumber()) {
            const errorCode = iti.getValidationError();
            const msg = errorMap[errorCode] || "Invalid number";
            showPhoneError(form, msg);
            return;
        }

        if (isOnlyCountries(form, only_countries_value, iti.getSelectedCountryData().iso2)) {
            return;
        }

        preloader.classList.remove('hidden');
        phone.value = iti.getNumber();

        switch (country.value) {
            case 'phone':
                country.value = iti.getSelectedCountryData().iso2.toUpperCase();
                break;
            case 'ip':
                try {
                    country.value = await getCountryByIP();
                } catch (error) {
                    console.error('Error fetching country by IP:', error);
                    country.value = 'UA';
                }
                break;
            case '':
                country.value = 'UA';
                break;
        }

        if (language.value === 'auto') {
            language.value = getLanguageByGeo(country.value);
        }

        const formData = new FormData(form);
        formData.append('js_token', Math.random().toString(36).substring(2, 15));
        const action = form.action;

        fetch(action, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                const url = `Thanks.php?language=${encodeURIComponent(data.lead_language)}&phone=${encodeURIComponent(data.fullphone)}&pfb=${encodeURIComponent(data.pfb)}&click_id=${encodeURIComponent(data.click_id)}&redirect_url=${encodeURIComponent(data.redirect_url)}`;
                window.location.href = url;
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
                preloader.classList.add('hidden');
            });
    });
}

forms.forEach(form => setupFormValidation(form));
