from json import dumps as json_dumps
import random
import os
from datetime import datetime as dt
import requests

from PIL import Image as ProcessImage
from resize_and_crop import resize_and_crop

import flask

from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField, ImageUploadField
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import helpers as admin_helpers
from flask_admin.form import rules

from flask_babelex import Babel, gettext

from wtforms.fields import TextField, PasswordField
from werkzeug.utils import secure_filename

from flask_ckeditor import CKEditor, CKEditorField

from werkzeug.exceptions import HTTPException
#from flask_basicauth import BasicAuth

from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password

#custom config
import config

app = flask.Flask(__name__)

babel = Babel(app)

#bcrypt = Bcrypt(app)
app.secret_key = config.secret_key

app.config['CKEDITOR_PKG_TYPE'] = 'full'

ckeditor = CKEditor(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + config.db_file
app.config['JSON_AS_ASCII'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+config.db_user+':'+config.db_pass+'@'+config.db_addr+'/'+config.db_name+'?charset=utf8mb4'
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['THUMBNAIL_FOLDER'] = config.THUMBNAIL_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024 #80mb max

# Flask-Security config
app.config['SECURITY_PASSWORD_HASH'] = "pbkdf2_sha512"
app.config['SECURITY_PASSWORD_SALT'] = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
app.config['SECURITY_LOGIN_URL'] = "/login/"
app.config['SECURITY_LOGOUT_URL'] = "/logout/"
app.config['SECURITY_REGISTER_URL'] = "/register/"

app.config['SECURITY_POST_LOGIN_VIEW'] = "/admin/"
app.config['SECURITY_POST_LOGOUT_VIEW'] = "/admin/"
app.config['SECURITY_POST_REGISTER_VIEW'] = "/admin/"

# Flask-Security features
app.config['SECURITY_REGISTERABLE'] = False
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

db = SQLAlchemy(app)

#app.config['BASIC_AUTH_USERNAME'] = config.login
#app.config['BASIC_AUTH_PASSWORD'] = config.password

#basic_auth = BasicAuth(app)

@babel.localeselector
def get_locale():
	if 'language' in flask.session:
		if flask.session['language']:
			return flask.session['language']
		else:
			return flask.request.accept_languages.best_match(config.LANGUAGES.keys())
	else:
		return flask.request.accept_languages.best_match(config.LANGUAGES.keys())

#------------------------<databases classes>------------------------------

class Setting(db.Model):

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(80))
	descr = db.Column(db.String(80))
	value = db.Column(db.Text)

	def __repr__(self):
		return self.name

class Gallery(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(80))
	details = db.Column(db.String(128))
	video = db.Column(db.Text)
	images = db.relationship('Gallery_Image', backref='good', lazy=True)

	def __repr__(self):
		return self.name

class Gallery_Image(db.Model):

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))
	file_name = db.Column(db.Text)

	def __repr__(self):
		return self.file_name

class Slider(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	img = db.Column(db.Text)
	title = db.Column(db.String(80))
	text = db.Column(db.Text)
	dark = db.Column(db.Boolean)
	video = db.Column(db.String())

	def __repr__(self):
		return self.title

class BlogType(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String())
	bloggers = db.relationship('Blogger', backref='blog_type', lazy=True)

	def __repr__(self):
		return self.name

class Blogger(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	instagram_link = db.Column(db.String())
	subs = db.Column(db.Integer)
	gender = db.Column(db.String())
	age = db.Column(db.Integer)
	city = db.Column(db.String())
	blog_type_id = db.Column(db.Integer, db.ForeignKey('blog_type.id'))
	stats = db.Column(db.String())
	phonenumber = db.Column(db.String())
	is_member = db.Column(db.Boolean)
	date_of_birth = db.Column(db.DateTime())
	stories_price = db.Column(db.String())
	post_price = db.Column(db.String())
	extra_accounts = db.Column(db.String())
	blog_theme = db.Column(db.String())
	full_name = db.Column(db.String())
	avg_views_stories = db.Column(db.Integer)

	def __repr__(self):
		if self.full_name:
			return self.full_name
		else:
			return 'Blogger with id ' + str(self.id)

class Employers(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	img = db.Column(db.String(190))
	name_uk = db.Column(db.String(190))
	name_ru = db.Column(db.String(190))
	name_en = db.Column(db.String(190))
	position_uk = db.Column(db.String(190))
	position_ru = db.Column(db.String(190))
	position_en = db.Column(db.String(190))

	def __repr__(self):
		return self.name_uk

class Request(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(190))
	surname = db.Column(db.String(190))
	link = db.Column(db.String(190))
	city = db.Column(db.String(190))
	phone = db.Column(db.String(190))
	email = db.Column(db.String(190))
	photo = db.Column(db.String(190))
	statement = db.Column(db.String(190))

	def __repr__(self):
		return self.name + self.surname

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(190))
	img = db.Column(db.Text)
	date = db.Column(db.DateTime)
	place = db.Column(db.String(190))
	description = db.Column(db.Text)
	short = db.Column(db.String())

	def __repr__(self):
		return self.name

roles_users = db.Table(
	'roles_users',
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
	db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

	def __str__(self):
		return self.name


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(255))
	last_name = db.Column(db.String(255))
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	roles = db.relationship('Role', secondary=roles_users,
							backref=db.backref('users', lazy='dynamic'))

	def __str__(self):
		return self.email

	def set_password(self, password):
		self.password = encrypt_password(password)

db.create_all()

#------------------/database classes/---------------------------

# setup security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#------------------<flask_admin>--------------------------------

#class AuthException(HTTPException):
#	def __init__(self, message):
#		 super().__init__(message, flask.Response(
#			 message, 401,
#			 {'WWW-Authenticate': 'Basic realm="Login Required"'}
#		 ))

def get_current_user():
	from flask.ext.security import current_user
	try:
		return User.objects.get(id=current_user.id)
	except Exception as e:
		# logger.warning("No user found: %s", str(e))
		return current_user


def is_accessible(roles_accepted=None, user=None):
	user = user or get_current_user()
	# uncomment if "admin" has access to everything
	# if user.has_role('admin'):
	#	 return True
	if roles_accepted:
		accessible = any(
			[user.has_role(role) for role in roles_accepted]
		)
		return accessible
	return True


class Roled(object):

	def is_accessible(self):
		roles_accepted = getattr(self, 'roles_accepted', None)
		return is_accessible(roles_accepted=roles_accepted, user=current_user)

	def _handle_view(self, name, *args, **kwargs):
		if not current_user.is_authenticated:
			return redirect(url_for_security('login', next="/admin"))
		if not self.is_accessible():
			# return self.render("admin/denied.html")
			return "<p>Access denied</p>"

class AdminView(Roled, ModelView):

	def __init__(self, *args, **kwargs):
		self.roles_accepted = kwargs.pop('roles_accepted', list())
		super(AdminView, self).__init__(*args, **kwargs)

#restict access to /admin index
class MyAdminIndexView(AdminIndexView):

	def is_accessible(self):
		return (current_user.is_active and
				current_user.is_authenticated and
				current_user.has_role('user')
		)

	def _handle_view(self, name, **kwargs):
		"""
		Override builtin _handle_view in order to redirect users when a view is not accessible.
		"""
		if not self.is_accessible():
			if current_user.is_authenticated:
				# permission denied
				flask.abort(403)
			else:
				# login
				return flask.redirect(flask.url_for('security.login',
													next=flask.request.url
													))

	def is_visible(self):
		return False

def prefix_name(obj=None, file_data=''):
	hash = random.getrandbits(128)
	ext = file_data.filename.split('.')[-1]
	path = '%s.%s' % (hash, ext)
	return path

def prefix_name_blogger(obj=None, file_data=''):
	hash = random.getrandbits(128)
	ext = file_data.filename.split('.')[-1]
	path = '%s.%s' % (hash, ext)
	print(path)
	return os.path.join('uploads', path)

def thumb_name(file_data):
	return os.path.join('thumbnails', file_data)

def count_instagram_followers(url):
	try:
		response = requests.get(url)
	except:
		return

	if response.status_code != 200:
		return

	search_string = '"edge_followed_by":{"count":'
	start_index = response.text.find(search_string) + len(search_string)
	end_index = response.text.find('}', start_index)
	follower_count = response.text[start_index:end_index]

	return int(follower_count)

#list of users in admin
class SliderView(AdminView):
	column_labels = dict(title='Наименование',
						text='Текст',
						video='Видео',
						mute='Видео без звука',
						dark='Светлый текст (если фото темное)'
					)

	form_overrides = {
		'img': ImageUploadField,
		'video': FileUploadField
	}

	column_list = ('title', 'text')

	form_args = {
		'video':{
		'label':'Видео',
		'base_path': 'static/uploads',
		'namegen': prefix_name
		},
		'img': {
			'label': 'Изображение',
			'base_path': 'static/uploads',
			'allow_overwrite': True,
			'namegen': prefix_name,
			'thumbnail_size': (256,256, True),
			'thumbgen' : thumb_name
		}
	}

class BloggersViewUser(AdminView):
	column_labels = dict(instagram_link='Аккаунт',
						subs='Подписчики',
						gender='Пол',
						age='Возраст',
						city='Город проживания',
						blog_type='Тип аккаунта',
						stats='Статистика',
						phonenumber='Номер для связи',
						is_member='Член ассоциации',
						date_of_birth='Дата рождения',
						extra_accounts='Другие аккаунты',
						blog_theme='Тема блога',
						full_name='ФИО, если ребёнок, то ФИО родителя',
						avg_views_stories='Среднее кол-во просмотров сторис'
					)

	list_template = 'admin/new_blogger.html'

	form_overrides = {
		'stats': ImageUploadField
	}

	form_choices = {
		'gender': [
			('Мужской','Мужской',),
			('Женский','Женский',)
		]
	}

	form_args = {
		'stats': {
			'base_path': 'static',
			'allow_overwrite': True,
			'namegen': prefix_name_blogger
		}
	}

	form_excluded_columns = ('post_price', 'stories_price')


class BloggersViewAdmin(AdminView):
	column_labels = dict(instagram_link='Аккаунт',
						subs='Подписчики',
						gender='Пол',
						age='Возраст',
						city='Город проживания',
						blog_type='Тип аккаунта',
						stats='Статистика',
						phonenumber='Номер для связи',
						is_member='Член ассоциации',
						date_of_birth='Дата рождения',
						stories_price='Цена сторис',
						post_price='Цена поста',
						extra_accounts='Другие аккаунты',
						blog_theme='Тема блога',
						full_name='ФИО',
						avg_views_stories='Среднее кол-во просмотров сторис'
					)

	column_list = ('full_name', 'gender', 'city', 'blog_type', 'phonenumber', 'is_member')


	column_searchable_list = ('full_name','city','phonenumber','instagram_link', 'blog_type.name', )

	can_export = True

	form_overrides = {
		'stats': ImageUploadField
	}

	form_choices = {
		'gender': [
			('Мужской','Мужской',),
			('Женский','Женский',)
		]
	}

	form_args = {
		'stats': {
			'base_path': 'static',
			'allow_overwrite': True,
			'namegen': prefix_name_blogger
		}
	}

	def on_form_prefill(self, form, id):
		url = self.model.query.filter_by(id=id).first().instagram_link
		if url and url != ' ' and url.startswith('https://'):
			count = count_instagram_followers(url)
			if count:
				form.subs.data = count
			else:
				pass
		else:
			pass


class DefView(AdminView):
	pass

class SettingsView(AdminView):
	form_extra_fields = {
		'file': FileUploadField('file', base_path = os.path.dirname(os.path.abspath(__file__)) + app.config['UPLOAD_FOLDER'], namegen = prefix_name)
	}

	form_widget_args = {
		'name': {
			'readonly': True
		},
	}

	column_list = ('name', 'descr', 'value')

	def on_model_change(self, form, Setting, is_created=False):
		if form.file.data:
			#form.file.data.save(os.path.dirname(os.path.abspath(__file__)) + os.path.join(app.config['UPLOAD_FOLDER'], form.file.data.filename))
			Setting.value = os.path.join(app.config['UPLOAD_FOLDER'], form.file.data.filename)

class GalleryView(AdminView):
	form_extra_fields = {
		'temp_field': TextField('Загрузить фото (несколько)')
	}

	column_labels = dict(name='Наименование', images='Изображения', video='Ссылка на видео', details='Описание')

	form_columns = ('images', 'temp_field', 'name', 'details', 'video')

	create_template = 'admin_edit.html'
	edit_template = 'admin_edit.html'

class RequestView(AdminView):
	column_labels = dict(name='Имя', surname='Фамилия', link='Ссылка', city='Город', phone='Телефон', photo='Фотография', statement='Скан заявки')

	column_list = ('name', 'surname', 'city', 'link', 'phone')

	create_template = 'req_admin_edit.html'
	edit_template = 'req_admin_edit.html'

class EventView(AdminView):
	form_overrides = dict(description=CKEditorField, img = ImageUploadField)
	column_labels = dict(name='Название', date='Дата', place='Место', description='Описание', short='Краткое описание')
	form_columns = ('name', 'img', 'date', 'place', 'short', 'description', 'temp_field')
	column_list = ('name', 'date', 'place')

	form_extra_fields = {
		'temp_field': TextField('Загрузить изобаражение в текстовый редактор')
	}

	form_args = {
		'img': {
			'label': 'Изображение',
			'base_path': 'static/uploads',
			'allow_overwrite': True,
			'namegen': prefix_name,
			'thumbnail_size': (420,420, True),
			'thumbgen' : thumb_name
		}
	}

	create_template = 'admin_image.html'
	edit_template = 'admin_image.html'

class UserView(AdminView):

	form_excluded_columns = ('password')

	form_extra_fields = {
		'password2': PasswordField('Password')
	}

	def on_model_change(self, form, User, is_created):
		if form.password2.data is not None and form.password2.data != ' ':
			User.set_password(form.password2.data)


#initialize admin views
admin = Admin(app, name='Панель управления', template_mode='bootstrap3', index_view=MyAdminIndexView(), url='/', base_template='my_master.html',)
admin.add_view(SettingsView(Setting, db.session, 'Основные', url='/admin/settings', category='Настройки', roles_accepted=['superuser']))
admin.add_view(GalleryView(Gallery, db.session, 'Галерея', url='/admin/gallery', roles_accepted=['superuser']))
admin.add_view(SliderView(Slider, db.session, 'Слайдер', url='/admin/slider', roles_accepted=['superuser']))
admin.add_view(BloggersViewAdmin(Blogger, db.session, 'Блогеры', url='/admin/bloggers', category='Блогеры', roles_accepted=['superuser']))
admin.add_view(BloggersViewUser(Blogger, db.session, 'Новый блогер', url='/admin/bloggers_new', endpoint='bloggers_new', roles_accepted=['user']))
admin.add_view(DefView(BlogType, db.session, 'Категории', url='/admin/bloggertypes', category='Блогеры', roles_accepted=['superuser']))
admin.add_view(RequestView(Request, db.session, 'Заявки', url='/admin/requests', roles_accepted=['superuser']))
admin.add_view(EventView(Event, db.session, 'События', url='/admin/events', roles_accepted=['superuser']))
admin.add_view(DefView(Employers, db.session, 'Сотрудники', url='/admin/employers', category='Настройки', roles_accepted=['superuser']))
admin.add_view(UserView(User, db.session, 'Пользователи', url='/admin/users', category='Настройки', roles_accepted=['superuser']))
admin.add_view(DefView(Role, db.session, 'Роли', url='/admin/roles', category='Настройки', roles_accepted=['superuser']))


#path = os.path.join(os.path.dirname(__file__), 'static/uploads')
#admin.add_view(FileAdmin(path, '/static/uploads/', name='Файлы', category='Настройки'))
#---------------------/flask_admin/---------------------

@security.context_processor
def security_context_processor():
	return dict(
		admin_base_template=admin.base_template,
		admin_view=admin.index_view,
		h=admin_helpers,
		get_url=flask.url_for
	)

@app.route('/language/<language>')
def set_language(language=None):
	if language in config.LANGUAGES:
		flask.session['language'] = language
	return flask.redirect(flask.url_for('index'))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/save_image_ck', methods=["GET","POST"])
def save_image_ck():
	if 'files[]' not in flask.request.files:
		resp = flask.jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp

	files = flask.request.files.getlist('files[]')

	errors = {}
	success = False
	filenames = []

	for file in files:
		if file and allowed_file(file.filename):
			filename = prefix_name(file_data=file)
			file.save(os.path.dirname(os.path.abspath(__file__)) + os.path.join(app.config['UPLOAD_FOLDER'], filename))
			success = True
			filenames.append(filename)
		else:
			errors[file.filename] = 'File type is not allowed'

	if success and errors:
		errors['message'] = 'File(s) successfully uploaded'
		errors['filenames'] = filenames
		resp = flask.jsonify(errors)
		resp.status_code = 206
		return resp
	if success:
		resp = flask.jsonify({'message' : 'Files successfully uploaded', 'filenames':filenames})
		resp.status_code = 201
		return resp
	else:
		resp = flask.jsonify(errors)
		resp.status_code = 400
		return resp

@app.route('/save_image', methods=["GET","POST"])
def save_image():
	if 'files[]' not in flask.request.files:
		resp = flask.jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp

	files = flask.request.files.getlist('files[]')

	errors = {}
	success = False
	filenames = []

	for file in files:
		if file and allowed_file(file.filename):
			filename = prefix_name(file_data=file)
			file.save(os.path.dirname(os.path.abspath(__file__)) + os.path.join(app.config['UPLOAD_FOLDER'], filename))
			with resize_and_crop(os.path.dirname(os.path.abspath(__file__)) + os.path.join(app.config['UPLOAD_FOLDER'], filename), (512,512), "middle") as image:
				#image.thumbnail((240, 240), ProcessImage.ANTIALIAS)
				image.save(os.path.dirname(os.path.abspath(__file__)) + os.path.join(config.THUMBNAIL_FOLDER, filename)) #and save it
			success = True
			filenames.append(filename)
			if flask.request.args.get('id') != 'null':
				good_id = flask.request.args.get('id')
			else:
				try:
					good_id = Gallery.query.order_by(Gallery.id.desc()).first().id + 1
				except:
					good_id = 1
			#print(good_id)
			new_image = Gallery_Image(gallery_id = int(good_id), file_name = filename)
			db.session.add(new_image)
			db.session.commit()

		else:
			errors[file.filename] = 'File type is not allowed'

	if success and errors:
		errors['message'] = 'File(s) successfully uploaded'
		errors['filenames'] = filenames
		resp = flask.jsonify(errors)
		resp.status_code = 206
		return resp
	if success:
		resp = flask.jsonify({'message' : 'Files successfully uploaded', 'filenames':filenames})
		resp.status_code = 201
		return resp
	else:
		resp = flask.jsonify(errors)
		resp.status_code = 400
		return resp

def get_settings():
	as_dict = {}
	for i in Setting.query.all():
		as_dict[i.name] = i.value

	return as_dict

@app.route('/get_events', methods=['GET'])
def get_events():
	result = {}
	for event in Event.query.all():
		result[event.date.strftime('%m-%d-%Y')] = "<a href='/event/"+str(event.id)+"'>"+event.name+"</a>"

	resp = flask.jsonify(result)
	resp.status_code = 201
	return resp

@app.route('/event/<event_id>', methods=['GET'])
def event(event_id):
	return flask.render_template('event.html',
				settings = get_settings(),
				event = Event.query.get(event_id),
				locale=get_locale())

@app.route("/", methods=["GET"])
def index():
	print(get_locale())
	return flask.render_template("index.html",
				settings = get_settings(),
				gallery = Gallery.query.order_by(Gallery.id.desc()).limit(3).all(),
				employers = Employers.query.all(),
				slider = Slider.query.all(),
				locale=get_locale(),
				events=Event.query.order_by(Event.id.desc()).limit(5).all())

@app.route('/partners', methods=['GET'])
def partners():
	return flask.render_template("partners.html",
				settings = get_settings(),
				locale=get_locale())

@app.route('/join', methods=['GET'])
def join():
	return flask.render_template("join.html",
				settings = get_settings(),
				locale=get_locale())

@app.route('/join', methods=['POST'])
def join_post():
	files = flask.request.files
	if 'scan' not in files or 'photo' not in files:
		flask.flash(gettext('Не приложены необходимые документы'))
		return flask.redirect(flask.url_for('join'))

	if files['scan'] and allowed_file(files['scan'].filename):
			scan_filename = prefix_name(file_data=files['scan'])
			files['scan'].save(os.path.dirname(os.path.abspath(__file__)) + os.path.join(app.config['UPLOAD_FOLDER'], scan_filename))
	else:
		flask.flash(gettext('Не приложены необходимые документы'))
		return flask.redirect(flask.url_for('join'))

	if files['photo'] and allowed_file(files['photo'].filename):
			photo_filename = prefix_name(file_data=files['photo'])
			files['photo'].save(os.path.dirname(os.path.abspath(__file__)) + os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
	else:
		flask.flash(gettext('Не приложены необходимые документы'))
		return flask.redirect(flask.url_for('join'))

	try:
		f = flask.request.form
		new_request = Request(name = f['name'],
							surname = f['lastname'],
							link = f['link'],
							city = f['city'],
							phone = f['phone'],
							email = f['email'],
							photo = photo_filename,
							statement = scan_filename)

		db.session.add(new_request)
		db.session.commit()
	except Exception as e:
		print(e)
		flask.flash(gettext('Что-то пошло не так, попробуйте снова позже'))
		return flask.redirect(flask.url_for('join'))
	finally:
		flask.flash(gettext('Заявка успешно отправлена'))
		return flask.redirect(flask.url_for('join'))


@app.route('/bloggers', methods=['GET'])
def bloggers():
	return flask.render_template("bloggers.html",
				settings = get_settings(),
				bloggers = Blogger.query.all(),
				locale=get_locale())

@app.route('/map', methods=['GET'])
def map():
	return flask.render_template("map.html",
				settings = get_settings(),
				locale=get_locale())

@app.route("/get_gallery_<num>", methods=["GET"])
def get_gallery(num):
	posts = Gallery.query.order_by(Gallery.id.desc()).limit(3*int(num)).all()
	posts = posts[(int(num)*3)-3:]
	result = ''
	for p_num, post in enumerate(posts):
		if not post.name:
			post.name = ''

		result += '<article class="portfolio-item col-lg-4 col-md-4 col-sm-6 col-12"><div class="grid-inner"><div class="portfolio-image" style="margin-top:'
		if (p_num+1) % 3 == 1:
			result += '65px;'
		elif (p_num+1) % 3 == 2:
			result += '0px;'
		elif (p_num+1) % 3 == 0:
			result += '115px;'
		result +='">'
		if len(post.images) > 1:
			result +='<div class="fslider" data-arrows="false" data-speed="400" data-pause="4000"><div class="flexslider"><div class="slider-wrap">'
			for image in post.images:
				result += '<div class="slide"><a href="portfolio-single-gallery.html"><img src="'+app.config['THUMBNAIL_FOLDER']+'/'+image.file_name+'" alt="'+post.name+'"></a></div>'
			result +='</div></div></div>'
		else:
			result += '<a href="portfolio-single.html">'
			if post.images:
				result +='<img src="'+app.config['THUMBNAIL_FOLDER']+'/'+post.images[0].file_name+'" alt="'+post.name+'">'
			result +='</a>'
		result +='<div class="bg-overlay"'
		if len(post.images) > 1:
			result += 'data-lightbox="gallery"'
		result +='><div class="bg-overlay-content dark" data-hover-animate="fadeIn">'
		if post.video:
			result += '<a href="'+post.video+'" class="overlay-trigger-icon bg-light text-dark" data-hover-animate="fadeInDownSmall" data-hover-animate-out="fadeOutUpSmall" data-hover-speed="350" data-lightbox="iframe"><i class="icon-line-play"></i></a>'
		if len(post.images) > 1:
			for index, image in enumerate(post.images):
				if index == 0:
					result += '<a href="'+app.config['UPLOAD_FOLDER']+'/'+image.file_name+'" class="overlay-trigger-icon bg-light text-dark" data-hover-animate="fadeInDownSmall" data-hover-animate-out="fadeOutUpSmall" data-hover-speed="350" data-lightbox="gallery-item"><i class="icon-line-stack-2"></i></a>'
				else:
					result +='<a href="'+app.config['UPLOAD_FOLDER']+'/'+image.file_name+'" class="d-none" data-lightbox="gallery-item"></a>'''
		else:
			if post.images:
				result += '<a href="'+app.config['UPLOAD_FOLDER']+'/'+post.images[0].file_name+'" class="overlay-trigger-icon bg-light text-dark" data-hover-animate="fadeInDownSmall" data-hover-animate-out="fadeOutUpSmall" data-hover-speed="350" data-lightbox="image" title="Image"><i class="icon-line-plus"></i></a>'
		result += '''<a href="portfolio-single.html" class="overlay-trigger-icon bg-light text-dark" data-hover-animate="fadeInDownSmall" data-hover-animate-out="fadeOutUpSmall" data-hover-speed="350"><i class="icon-line-ellipsis"></i></a>
		</div>
		<div class="bg-overlay-bg dark" data-hover-animate="fadeIn"></div>
		</div>
		</div>
		<div class="portfolio-desc">
		<h3><a href="portfolio-single.html">'''+post.name+'''</a></h3>'''
		if post.details:
			result +='<span>'+post.details+'</span>'
		result +='</div></div></article>'

	if not Gallery.query.order_by(Gallery.id.desc()).first() in posts:
		result+= '<a href="/get_gallery_2" class="button button-dark button-rounded load-next-portfolio" style="color: #F7F7F7;">Загрузить еще...</a>'

	return result

def create_admin(password='admin'):
	with app.app_context():
		if not Role.query.filter_by(name='user').first() or not Role.query.filter_by(name='superuser').first():
			user_role = Role(name='user')
			super_user_role = Role(name='superuser')
			db.session.add(user_role)
			db.session.add(super_user_role)
			db.session.commit()
		else:
			user_role = Role.query.filter_by(name='user').first()
			super_user_role = Role.query.filter_by(name='superuser').first()

		test_user = user_datastore.create_user(
			first_name='Admin',
			email='admin',
			password=encrypt_password(password),
			roles=[user_role, super_user_role]
		)
		db.session.commit()
		return 'Succ'
