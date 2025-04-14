from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

VALID_TOKEN = "supersecrettoken123"

capital_timezones = {
    "Kabul": "Asia/Kabul",  # Afghanistan
    "Tirana": "Europe/Tirane",  # Albania
    "Algiers": "Africa/Algiers",  # Algeria
    "Andorra la Vella": "Europe/Andorra",  # Andorra
    "Luanda": "Africa/Luanda",  # Angola
    "Saint John's": "America/Antigua",  # Antigua and Barbuda
    "Buenos Aires": "America/Argentina/Buenos_Aires",  # Argentina
    "Yerevan": "Asia/Yerevan",  # Armenia
    "Canberra": "Australia/Sydney",  # Australia
    "Vienna": "Europe/Vienna",  # Austria
    "Baku": "Asia/Baku",  # Azerbaijan
    "Nassau": "America/Nassau",  # Bahamas
    "Manama": "Asia/Bahrain",  # Bahrain
    "Dhaka": "Asia/Dhaka",  # Bangladesh
    "Bridgetown": "America/Barbados",  # Barbados
    "Minsk": "Europe/Minsk",  # Belarus
    "Brussels": "Europe/Brussels",  # Belgium
    "Belmopan": "America/Belize",  # Belize
    "Porto-Novo": "Africa/Porto-Novo",  # Benin
    "Thimphu": "Asia/Thimphu",  # Bhutan
    "La Paz": "America/La_Paz",  # Bolivia (seat of government)
    "Sucre": "America/La_Paz",  # Bolivia (constitutional capital)
    "Sarajevo": "Europe/Sarajevo",  # Bosnia and Herzegovina
    "Gaborone": "Africa/Gaborone",  # Botswana
    "Brasilia": "America/Sao_Paulo",  # Brazil
    "Bandar Seri Begawan": "Asia/Brunei",  # Brunei
    "Sofia": "Europe/Sofia",  # Bulgaria
    "Ouagadougou": "Africa/Ouagadougou",  # Burkina Faso
    "Gitega": "Africa/Bujumbura",  # Burundi
    "Phnom Penh": "Asia/Phnom_Penh",  # Cambodia
    "Yaounde": "Africa/Douala",  # Cameroon
    "Ottawa": "America/Toronto",  # Canada
    "Praia": "Atlantic/Cape_Verde",  # Cape Verde
    "Bangui": "Africa/Bangui",  # Central African Republic
    "N'Djamena": "Africa/Ndjamena",  # Chad
    "Santiago": "America/Santiago",  # Chile
    "Beijing": "Asia/Shanghai",  # China
    "Bogota": "America/Bogota",  # Colombia
    "Moroni": "Indian/Comoro",  # Comoros
    "Brazzaville": "Africa/Brazzaville",  # Republic of the Congo
    "Kinshasa": "Africa/Kinshasa",  # Democratic Republic of the Congo
    "San Jose": "America/Costa_Rica",  # Costa Rica
    "Yamoussoukro": "Africa/Abidjan",  # Côte d'Ivoire (official)
    "Abidjan": "Africa/Abidjan",  # Côte d'Ivoire (de facto)
    "Zagreb": "Europe/Zagreb",  # Croatia
    "Havana": "America/Havana",  # Cuba
    "Nicosia": "Asia/Nicosia",  # Cyprus
    "Prague": "Europe/Prague",  # Czechia
    "Copenhagen": "Europe/Copenhagen",  # Denmark
    "Djibouti": "Africa/Djibouti",  # Djibouti
    "Roseau": "America/Dominica",  # Dominica
    "Santo Domingo": "America/Santo_Domingo",  # Dominican Republic
    "Quito": "America/Guayaquil",  # Ecuador
    "Cairo": "Africa/Cairo",  # Egypt
    "San Salvador": "America/El_Salvador",  # El Salvador
    "Malabo": "Africa/Malabo",  # Equatorial Guinea
    "Asmara": "Africa/Asmara",  # Eritrea
    "Tallinn": "Europe/Tallinn",  # Estonia
    "Mbabane": "Africa/Mbabane",  # Eswatini (administrative)
    "Lobamba": "Africa/Mbabane",  # Eswatini (royal/legislative)
    "Addis Ababa": "Africa/Addis_Ababa",  # Ethiopia
    "Suva": "Pacific/Fiji",  # Fiji
    "Helsinki": "Europe/Helsinki",  # Finland
    "Paris": "Europe/Paris",  # France
    "Libreville": "Africa/Libreville",  # Gabon
    "Banjul": "Africa/Banjul",  # Gambia
    "Tbilisi": "Asia/Tbilisi",  # Georgia
    "Berlin": "Europe/Berlin",  # Germany
    "Accra": "Africa/Accra",  # Ghana
    "Athens": "Europe/Athens",  # Greece
    "Saint George's": "America/Grenada",  # Grenada
    "Guatemala City": "America/Guatemala",  # Guatemala
    "Conakry": "Africa/Conakry",  # Guinea
    "Bissau": "Africa/Bissau",  # Guinea-Bissau
    "Georgetown": "America/Guyana",  # Guyana
    "Port-au-Prince": "America/Port-au-Prince",  # Haiti
    "Tegucigalpa": "America/Tegucigalpa",  # Honduras
    "Budapest": "Europe/Budapest",  # Hungary
    "Reykjavik": "Atlantic/Reykjavik",  # Iceland
    "New Delhi": "Asia/Kolkata",  # India
    "Jakarta": "Asia/Jakarta",  # Indonesia
    "Tehran": "Asia/Tehran",  # Iran
    "Baghdad": "Asia/Baghdad",  # Iraq
    "Dublin": "Europe/Dublin",  # Ireland
    "Jerusalem": "Asia/Jerusalem",  # Israel
    "Rome": "Europe/Rome",  # Italy
    "Kingston": "America/Jamaica",  # Jamaica
    "Tokyo": "Asia/Tokyo",  # Japan
    "Amman": "Asia/Amman",  # Jordan
    "Nur-Sultan": "Asia/Almaty",  # Kazakhstan (Astana, now Nur-Sultan)
    "Nairobi": "Africa/Nairobi",  # Kenya
    "Tarawa": "Pacific/Tarawa",  # Kiribati
    "Pyongyang": "Asia/Pyongyang",  # North Korea
    "Seoul": "Asia/Seoul",  # South Korea
    "Pristina": "Europe/Belgrade",  # Kosovo
    "Kuwait City": "Asia/Kuwait",  # Kuwait
    "Bishkek": "Asia/Bishkek",  # Kyrgyzstan
    "Vientiane": "Asia/Vientiane",  # Laos
    "Riga": "Europe/Riga",  # Latvia
    "Beirut": "Asia/Beirut",  # Lebanon
    "Maseru": "Africa/Maseru",  # Lesotho
    "Monrovia": "Africa/Monrovia",  # Liberia
    "Tripoli": "Africa/Tripoli",  # Libya
    "Vaduz": "Europe/Vaduz",  # Liechtenstein
    "Vilnius": "Europe/Vilnius",  # Lithuania
    "Luxembourg": "Europe/Luxembourg",  # Luxembourg
    "Antananarivo": "Indian/Antananarivo",  # Madagascar
    "Lilongwe": "Africa/Blantyre",  # Malawi
    "Kuala Lumpur": "Asia/Kuala_Lumpur",  # Malaysia
    "Malé": "Indian/Maldives",  # Maldives
    "Bamako": "Africa/Bamako",  # Mali
    "Valletta": "Europe/Malta",  # Malta
    "Majuro": "Pacific/Majuro",  # Marshall Islands
    "Nouakchott": "Africa/Nouakchott",  # Mauritania
    "Port Louis": "Indian/Mauritius",  # Mauritius
    "Mexico City": "America/Mexico_City",  # Mexico
    "Palikir": "Pacific/Pohnpei",  # Micronesia
    "Chisinau": "Europe/Chisinau",  # Moldova
    "Monaco": "Europe/Monaco",  # Monaco
    "Ulaanbaatar": "Asia/Ulaanbaatar",  # Mongolia
    "Podgorica": "Europe/Podgorica",  # Montenegro
    "Rabat": "Africa/Casablanca",  # Morocco
    "Maputo": "Africa/Maputo",  # Mozambique
    "Naypyidaw": "Asia/Yangon",  # Myanmar
    "Windhoek": "Africa/Windhoek",  # Namibia
    "Yaren": "Pacific/Nauru",  # Nauru
    "Kathmandu": "Asia/Kathmandu",  # Nepal
    "Amsterdam": "Europe/Amsterdam",  # Netherlands
    "Wellington": "Pacific/Auckland",  # New Zealand
    "Managua": "America/Managua",  # Nicaragua
    "Niamey": "Africa/Niamey",  # Niger
    "Abuja": "Africa/Lagos",  # Nigeria
    "Skopje": "Europe/Skopje",  # North Macedonia
    "Oslo": "Europe/Oslo",  # Norway
    "Muscat": "Asia/Muscat",  # Oman
    "Islamabad": "Asia/Karachi",  # Pakistan
    "Ngerulmud": "Pacific/Palau",  # Palau
    "Jerusalem": "Asia/Jerusalem",  # Palestine (see note)
    "Panama City": "America/Panama",  # Panama
    "Port Moresby": "Pacific/Port_Moresby",  # Papua New Guinea
    "Asuncion": "America/Asuncion",  # Paraguay
    "Lima": "America/Lima",  # Peru
    "Manila": "Asia/Manila",  # Philippines
    "Warsaw": "Europe/Warsaw",  # Poland
    "Lisbon": "Europe/Lisbon",  # Portugal
    "Doha": "Asia/Qatar",  # Qatar
    "Bucharest": "Europe/Bucharest",  # Romania
    "Moscow": "Europe/Moscow",  # Russia
    "Kigali": "Africa/Kigali",  # Rwanda
    "Basseterre": "America/St_Kitts",  # Saint Kitts and Nevis
    "Castries": "America/St_Lucia",  # Saint Lucia
    "Kingstown": "America/St_Vincent",  # Saint Vincent and the Grenadines
    "Apia": "Pacific/Apia",  # Samoa
    "San Marino": "Europe/San_Marino",  # San Marino
    "Sao Tome": "Africa/Sao_Tome",  # Sao Tome and Principe
    "Riyadh": "Asia/Riyadh",  # Saudi Arabia
    "Dakar": "Africa/Dakar",  # Senegal
    "Belgrade": "Europe/Belgrade",  # Serbia
    "Victoria": "Indian/Mahe",  # Seychelles
    "Freetown": "Africa/Freetown",  # Sierra Leone
    "Singapore": "Asia/Singapore",  # Singapore
    "Bratislava": "Europe/Bratislava",  # Slovakia
    "Ljubljana": "Europe/Ljubljana",  # Slovenia
    "Honiara": "Pacific/Guadalcanal",  # Solomon Islands
    "Mogadishu": "Africa/Mogadishu",  # Somalia
    "Pretoria": "Africa/Johannesburg",  # South Africa (administrative)
    "Juba": "Africa/Juba",  # South Sudan
    "Madrid": "Europe/Madrid",  # Spain
    "Colombo": "Asia/Colombo",  # Sri Lanka
    "Khartoum": "Africa/Khartoum",  # Sudan
    "Paramaribo": "America/Paramaribo",  # Suriname
    "Stockholm": "Europe/Stockholm",  # Sweden
    "Bern": "Europe/Zurich",  # Switzerland
    "Damascus": "Asia/Damascus",  # Syria
    "Taipei": "Asia/Taipei",  # Taiwan
    "Dushanbe": "Asia/Dushanbe",  # Tajikistan
    "Dodoma": "Africa/Dar_es_Salaam",  # Tanzania
    "Bangkok": "Asia/Bangkok",  # Thailand
    "Lome": "Africa/Lome",  # Togo
    "Nuku'alofa": "Pacific/Tongatapu",  # Tonga
    "Port of Spain": "America/Port_of_Spain",  # Trinidad and Tobago
    "Tunis": "Africa/Tunis",  # Tunisia
    "Ankara": "Europe/Istanbul",  # Turkey
    "Ashgabat": "Asia/Ashgabat",  # Turkmenistan
    "Funafuti": "Pacific/Funafuti",  # Tuvalu
    "Kampala": "Africa/Kampala",  # Uganda
    "Kyiv": "Europe/Kyiv",  # Ukraine
    "Abu Dhabi": "Asia/Dubai",  # United Arab Emirates
    "London": "Europe/London",  # United Kingdom
    "Washington": "America/New_York",  # United States
    "Montevideo": "America/Montevideo",  # Uruguay
    "Tashkent": "Asia/Tashkent",  # Uzbekistan
    "Port Vila": "Pacific/Efate",  # Vanuatu
    "Vatican City": "Europe/Vatican",  # Vatican City
    "Caracas": "America/Caracas",  # Venezuela
    "Hanoi": "Asia/Ho_Chi_Minh",  # Vietnam
    "Sanaa": "Asia/Aden",  # Yemen
    "Lusaka": "Africa/Lusaka",  # Zambia
    "Harare": "Africa/Harare",  # Zimbabwe
}


@app.route("/time", methods=["GET"])
def get_time():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {VALID_TOKEN}":
        return jsonify({"error": "Unauthorized. Please provide a valid token."}), 401

    city = request.args.get("city")
    if not city:
        return jsonify(
            {"error": "Please provide a capital city via ?city=CapitalName"}
        ), 400

    timezone = capital_timezones.get(city)
    if not timezone:
        return jsonify({"error": f"Sorry, '{city}' is not in our database."}), 404

    tz = pytz.timezone(timezone)
    local_time = datetime.now(tz)
    utc_offset = local_time.strftime("%z")
    formatted_offset = f"UTC{utc_offset[:3]}:{utc_offset[3:]}"

    return jsonify(
        {
            "city": city,
            "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S"),
            "utc_offset": formatted_offset,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
