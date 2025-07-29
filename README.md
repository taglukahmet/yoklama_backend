# yoklama_backend


here is a dependecies list but to remind, most of them are downloaded under one main library, important ones are pointed explicitly in the list

# dependencies list:
aom=3.6.0=hd77b12b_0
asgiref=3.8.1=py312haa95532_0
*beautifulsoup4=4.13.4=py312haa95532_0*
brotlicffi=1.0.9.2=py312h5da7b33_1
bs4=4.13.4=py313hd3eb1b0_0
bzip2=1.0.8=h2bbff1b_6
ca-certificates=2025.2.25=haa95532_0
cairo=1.16.0=h85cdd14_6
certifi=2025.7.14=py312haa95532_0
cffi=1.17.1=py312h827c3e9_1
charset-normalizer=3.3.2=pyhd3eb1b0_0
click=8.1.8=py312haa95532_0
colorama=0.4.6=py312haa95532_0
dav1d=1.2.1=h2bbff1b_0
*django=5.2=py312haa95532_0*
*django-cors-headers=4.7.0=pyhd8ed1ab_0*
*django-phonenumber-field=8.1.0=pyhd8ed1ab_0*
*djangorestframework=3.16.0=pyhd8ed1ab_1*
*environs=14.2.0=pyhd8ed1ab_0*
expat=2.7.1=h8ddb27b_0
fontconfig=2.14.1=hb33846d_3
freeglut=3.4.0=h8a1e904_1
freetype=2.13.3=h0620614_0
fribidi=1.0.10=h62dcd97_0
graphite2=1.3.14=hd77b12b_1
harfbuzz=10.2.0=he2f9f60_1
icu=73.1=h6c2663c_0
idna=3.7=py312haa95532_0
jpeg=9e=h827c3e9_3
krb5=1.21.3=he4457a5_1
lcms2=2.16=h62be587_1
lerc=4.0.0=h5da7b33_0
libavif=1.1.1=h827c3e9_0
libdeflate=1.22=h2466b09_0
libffi=3.4.4=hd77b12b_1
libglib=2.84.2=h405b238_0
libiconv=1.16=h2bbff1b_3
libpng=1.6.39=h8cc25b3_0
libpq=17.4=h4a159e6_1
libtiff=4.7.0=h404307b_0
libwebp-base=1.3.2=h3d04722_1
libxml2=2.13.8=h866ff63_0
lz4-c=1.9.4=h2bbff1b_1
*marshmallow=4.0.0=py312haa95532_0*
openjpeg=2.5.2=h9b5d1b5_1
openssl=3.0.17=h35632f6_0
pcre2=10.42=h0ff8eda_1
*phonenumbers=8.13.49=py312haa95532_0*
pillow=11.3.0=py312hb328d1f_0
pip=25.1=pyhc872135_2
pixman=0.40.0=h2bbff1b_1
psycopg2=2.9.10=py312h827c3e9_0
psycopg2-binary=2.9.10=pyhd8ed1ab_1
pycparser=2.21=pyhd3eb1b0_0
pysocks=1.7.1=py312haa95532_0
*python=3.12.11=h716150d_0*
python-dotenv=1.1.0=py312haa95532_0
requests=2.32.4=py312haa95532_0
setuptools=78.1.1=py312haa95532_0
soupsieve=2.5=py312haa95532_0
sqlparse=0.5.2=py312haa95532_0
tk=8.6.14=h5e9d12e_1
typing-extensions=4.12.2=py312haa95532_0
typing_extensions=4.12.2=py312haa95532_0
tzdata=2025b=h04d1e81_0
ucrt=10.0.22621.0=haa95532_0
urllib3=2.5.0=py312haa95532_0
vc=14.3=h2df5915_10
vc14_runtime=14.44.35208=h4927774_10
vs2015_runtime=14.44.35208=ha6b5a95_10
wheel=0.45.1=py312haa95532_0
win_inet_pton=1.1.0=py312haa95532_0
xz=5.6.4=h4754444_1
zlib=1.2.13=h8cc25b3_1
zstd=1.5.6=h8880b57_0


also note that postgreSQL 17 is required due to some spesific lines in the codebase

# how to run and use:

1. open your terminal (whichever you use for python, I use anaconda prompt)
2. if its conda, activate your environment dedicated to the project
3. open the folder in the terminal
4. always make sure that you run these commands beforehand, because I may be making changes on some fileds:
   a. python manage.py makemigrations
   b. python manage.py migrate
5. then run "python manage.py runserver" and you are goood to go.
6. it will show you the localhost address, you will be using it for the frontend for local tests
