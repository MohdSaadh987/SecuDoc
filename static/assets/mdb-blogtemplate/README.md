# Blog template for Bootstrap 5


These templates were built with a **free Material Design UI Kit for the latest Bootstrap 5**.

<img height="25" src="https://mdbootstrap.com/img/Marketing/general/logo/medium/mdb-r.png">  [![GitHub Stars](https://img.shields.io/github/stars/mdbootstrap/mdb-ui-kit?label=Star%20now&style=social)](https://github.com/mdbootstrap/mdb-ui-kit/)

<a href="https://npmcharts.com/compare/mdbootstrap?minimal=true"> <img src="https://img.shields.io/npm/dm/mdbootstrap.svg?label=MDB%20Downloads" alt="Downloads"></a>
<a href="https://github.com/mdbootstrap/bootstrap-material-design/blob/master/License.pdf"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
<a href="https://twitter.com/intent/tweet/?text=Thanks+@mdbootstrap+for+creating+amazing+and+free+Material+Design+for+Bootstrap+4+UI+KIT%20https://mdbootstrap.com/docs/jquery/&hashtags=javascript,code,webdesign,bootstrap"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Let%20us%20know%20you%20were%20here%21&"></a>
<a href="https://www.youtube.com/watch?v=c9B4TPnak1A&t=6s"><img alt="YouTube Video Views" src="https://img.shields.io/youtube/views/c9B4TPnak1A?label=Bootstrap%205%20Tutorial%20Views&style=social"></a>
___

<table>
  <tbody>
    <tr>
      <td>
          <a href="https://mdbootstrap.com/freebies/blog/" alt="Bootstrap 5" rel="dofollow">
          		<img src="https://mdbcdn.b-cdn.net/wp-content/themes/mdbootstrap4/content/en/_mdb5/standard/freebies/blog/assets/featured.jpg">
          </a>
      </td>
      <td>
        <ul>
        <li><b>Built with the free MDB5 UI Kit</b></li>
         <li>Super simple, 1 minute implementation</li>
         <li><b>Plain javascript (but works also with jQuery)</b></li>
         <li>Use in your design and create amazing things</li>
         <li><b>MIT license - free for personal & commercial use</b></li>
          <li><b><a href="https://mdbootstrap.com/snippets/standard/mdbootstrap/2515504">Live Demo</a></b></li>
        </ul>
      </td>
    </tr>
   </tbody>
</table>


___

###### Discover tutorials for the latest Bootstrap 5 and learn how to create templates yourself.

**[>> Click here for a written tutorial](https://mdbootstrap.com/docs/standard/getting-started/quick-start/)**


<table>
  <tbody>
    <tr>
      <td align="center">
          		<img src="https://mdbootstrap.com/wp-content/uploads/2020/12/learnmore-1.png">
          </a>
      </td>
      <td>
          <a href="https://mdbootstrap.com/docs/standard/bootstrap-5-tutorial/#section-beginner" alt="Bootstrap 5" rel="dofollow">
          		<img src="https://mdbootstrap.com/wp-content/uploads/2020/12/cover-bootstrap-5-1.png">
          </a>
      </td>
    </tr>
     <tr>
        <td align="center">
          <p align="center"><b>Start to Code</b></p>
          <a href="https://mdbootstrap.com/docs/standard/bootstrap-5-tutorial/#section-beginner" alt="Bootstrap 5" rel="dofollow">
          		<img src="https://mdbootstrap.com/wp-content/uploads/2020/12/Screenshot_26.png">
          </a>
         </td>
        <td align="center">
          <p align="center"><b>Learn Bootstrap 5 | Crash Course for Beginners in 1.5H</b></p>
          <a href="https://mdbootstrap.com/docs/standard/bootstrap-5-tutorial/#section-beginner" alt="Bootstrap 5" rel="dofollow">
          		<img src="https://mdbootstrap.com/wp-content/uploads/2020/12/Screenshot_26.png">
          </a>
         </td>
      </tr>
   </tbody>
</table>

___
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_created', 'date_updated')  # Displayed fields in the list view

    def get_readonly_fields(self, request, obj=None):
        return ['title', 'description', 'date_created', 'date_updated', 'hashed_content']  # Make fields read-only

    def has_add_permission(self, request):
        return False  # Disable adding new posts

    def has_change_permission(self, request, obj=None):
        return False  # Disable changing existing posts

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting posts

    def get_list_display(self, request):
        # Exclude file_path from list_display
        return [field for field in self.list_display if field != 'file_path']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = [field.name for field in self.model._meta.fields]  # Make all fields read-only
        self.exclude = ['file_path']  # Exclude file_path from the form
        return super().change_view(request, object_id, form_url, extra_context)

    def file_path(self, instance):
        return "Hidden"  # Custom method to hide file_path

    file_path.short_description = 'File path'  # Customizing the column header in admin list view
    file_path.empty_value_display = 'Hidden'  # Display this when the field is empty or None







from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm
from .models import Post

# Unregister the existing UserAdmin
admin.site.unregister(User)

# Register UserAdmin with customizations
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm

    # Define list display fields if needed
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')

    # Define read-only fields
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ['username', 'password', 'first_name', 'last_name', 'email']
        else:  # Adding a new object
            return []

    # Optionally, define other admin behaviors
    def has_add_permission(self, request):
        return True  # Allow adding new users

    def has_change_permission(self, request, obj=None):
        return True  # Allow changing existing users

    def has_delete_permission(self, request, obj=None):
        return True  # Allow deleting users

# Register the PostAdmin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_created', 'date_updated')  # Displayed fields in the list view

    def get_readonly_fields(self, request, obj=None):
        return ['title', 'description', 'date_created', 'date_updated', 'hashed_content']  # Make fields read-only

    def has_add_permission(self, request):
        return False  # Disable adding new posts

    def has_change_permission(self, request, obj=None):
        return False  # Disable changing existing posts

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting posts

    def get_list_display(self, request):
        # Exclude file_path from list_display
        return [field for field in self.list_display if field != 'file_path']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = [field.name for field in self.model._meta.fields]  # Make all fields read-only
        self.exclude = ['file_path']  # Exclude file_path from the form
        return super().change_view(request, object_id, form_url, extra_context)

    def file_path(self, instance):
        return "Hidden"  # Custom method to hide file_path

    file_path.short_description = 'File path'  # Customizing the column header in admin list view
    file_path.empty_value_display = 'Hidden'  # Display this when the field is empty or None

















{% load static %}
{% load customfilter %}

{% block headerContent %}

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> {% if page_title %}
    <title>{{ page_title }} | File Management System</title>
    {% else %}
    <title>File Management System</title>
    {% endif %}
    <link rel="icon" href="{{ MEDIA_URL }}/default/logo.png">
    <link rel="stylesheet" href="{% static 'assets/font-awesome/css/all.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/bootstrap/css/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/select2/dist/css/select2.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/mdb-blogtemplate/css/mdb.min.css' %}" />
    <link rel="stylesheet" href="{% static 'assets/DataTables/datatables.min.css' %}" />
    <link rel="stylesheet" href="{% static 'assets/default/css/style.css' %}">

    <script src="{% static 'assets/font-awesome/js/all.min.js' %}"></script>
    <script src="{% static 'assets/default/js/jquery-3.6.0.min.js' %}"></script>
    <script src="{% static 'assets/bootstrap/js/bootstrap.min.js' %}"></script>
    <script src="{% static 'assets/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
    <script src="{% static 'assets/DataTables/datatables.min.js' %}"></script>
    <script src="{% static 'assets/bootstrap/js/popper.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'assets/mdb-blogtemplate/js/mdb.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'assets/default/js/script.js' %}"></script>
</head>
<style>
    main {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: auto;
    }
    .file-container {
        width: 100%;
        height: calc(100vh - 150px); /* Adjust height for header and footer */
        overflow-y: scroll;
        border: 1px solid #ccc;
        margin-bottom: 20px;
        position: relative; /* Position relative for overlay */
    }
    #file-content {
        display: block;
        margin: 0 auto;
    }
    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0); /* Transparent background */
        z-index: 1000; /* Ensure overlay is on top */
        pointer-events: none; /* Allow clicks to pass through to underlying elements */
    }
    #intro {
        margin-top: 58px;
    }
    @media (max-width: 991px) {
        #intro {
            margin-top: 45px;
        }
    }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const url = '{{ file_url }}';
        const extension = url.split('.').pop().toLowerCase();
        const fileContainer = document.getElementById('file-content');

        if (['png', 'jpg', 'jpeg', 'gif'].includes(extension)) {
            const img = document.createElement('img');
            img.src = url;
            img.classList.add('img-fluid');
            fileContainer.appendChild(img);
        } else if (['mp4', 'webm', 'ogg'].includes(extension)) {
            const video = document.createElement('video');
            video.src = url;
            video.controls = true;
            video.classList.add('video-fluid');
            fileContainer.appendChild(video);
        } else if (extension === 'pdf') {
            const pdfjsLib = window['pdfjs-dist/build/pdf'];
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';
            pdfjsLib.getDocument(url).promise.then(function(pdfDoc) {
                pdfDoc.getPage(1).then(function(page) {
                    const scale = 1.5;
                    const viewport = page.getViewport({ scale: scale });
                    const canvas = document.createElement('canvas');
                    const context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
                    const renderContext = {
                        canvasContext: context,
                        viewport: viewport
                    };
                    page.render(renderContext);
                    fileContainer.appendChild(canvas);
                });
            });
        }

        // Full screen toggle function
        function toggleFullScreen() {
            const elem = document.getElementById('file-container');
            if (!document.fullscreenElement) {
                elem.requestFullscreen().catch(err => {
                    alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
                });
            } else {
                document.exitFullscreen();
            }
        }

        // Prevent inspecting elements and right-clicking in full-screen mode
        document.addEventListener('fullscreenchange', function () {
            if (document.fullscreenElement) {
                document.fullscreenElement.addEventListener('contextmenu', function (event) {
                    event.preventDefault();
                });
                document.fullscreenElement.addEventListener('mousedown', function (event) {
                    event.preventDefault();
                });
                document.fullscreenElement.addEventListener('mouseup', function (event) {
                    event.preventDefault();
                });
            }
        });

        // Disable right-click and keyboard shortcuts for inspecting
        document.addEventListener('contextmenu', function(event) {
            event.preventDefault();
        });

        document.addEventListener('keydown', function(event) {
            if (event.key === 'F12' || (event.ctrlKey && event.shiftKey && event.key === 'I') || (event.ctrlKey && event.shiftKey && event.key === 'C') || (event.ctrlKey && event.shiftKey && event.key === 'J') || (event.ctrlKey && event.key === 'U')) {
                event.preventDefault();
            }
        });

        // Prevent selection and copying
        document.addEventListener('selectstart', function(event) {
            event.preventDefault();
        });

        document.addEventListener('copy', function(event) {
            event.preventDefault();
        });
    });
</script>
{% endblock headerContent %}

{% block pageContent %}

<nav class="navbar navbar-expand-lg navbar-light bg-white fixed-top shadow border-bottom">
    <div class="container">
        <!-- Navbar brand -->
        <a class="navbar-brand" target="_blank" href="">
            <img src="{{ MEDIA_URL }}/default/fms-logo.png" height="16" alt="{{ MEDIA_URL }}" loading="lazy" style="margin-top: -3px;" />
        </a>
        <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarExample01" aria-controls="navbarExample01" aria-expanded="false" aria-label="Toggle navigation">
            <i class="fas fa-bars"></i>
        </button>
    </div>
</nav>

<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card card-default border rounded-0">
            <div class="card-header">
                <h5 class="card-title"><b>Shared Document</b></h5>
            </div>
            <div class="card-body">
                <div class="container-fluid">
                    <div class="row mb-3">
                        <div class="col">
                            <dl>
                                <dt class="text-muted"><b>Title:</b></dt>
                                <dd class="ps-4">{{ post.title }}</dd>
                                <dt class="text-muted"><b>Description:</b></dt>
                                <dd class="ps-4">{{ post.description }}</dd>
                                <dt class="text-muted"><b>Uploaded By:</b></dt>
                                <dd class="ps-4">{{ post.user.username }}</dd>
                                <dt class="text-muted"><b>Filename:</b></dt>
                                <dd class="ps-4">{{ post.file_path|replaceBlank:'uploads/' }}</dd>
                            </dl>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <div class="file-container" id="file-container">
                                <div id="file-content"></div>
                                <div class="overlay"></div>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col text-center">
                            <button class="btn btn-primary" onclick="toggleFullScreen()">
                                <i class="fa fa-arrows-alt"></i> Toggle Full Screen
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<script>
    $(function() {
        $('#topNav .nav-link').each(function() {
            var current = '{{ request.get_full_path | urlencode }}'
            if (current == $(this).attr('href')) {
                $(this).parent().addClass('active')
            }
        })
    })
</script>
{% endblock pageContent %}




















/* Updated */

{% load static %}
{% load customfilter %}

{% block headerContent %}

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> {% if page_title %}
    <title>{{ page_title }} | SecuDoc</title>
    {% else %}
    <title>SecuDoc</title>
    {% endif %}
    <link rel="icon" href="{{ MEDIA_URL }}/default/logo.png">
    <link rel="stylesheet" href="{% static 'assets/font-awesome/css/all.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/bootstrap/css/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/select2/dist/css/select2.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/mdb-blogtemplate/css/mdb.min.css' %}" />
    <link rel="stylesheet" href="{% static 'assets/DataTables/datatables.min.css' %}" />
    <link rel="stylesheet" href="{% static 'assets/default/css/style.css' %}">

    <script src="{% static 'assets/font-awesome/js/all.min.js' %}"></script>
    <script src="{% static 'assets/default/js/jquery-3.6.0.min.js' %}"></script>
    <script src="{% static 'assets/bootstrap/js/bootstrap.min.js' %}"></script>
    <script src="{% static 'assets/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
    <script src="{% static 'assets/DataTables/datatables.min.js' %}"></script>
    <script src="{% static 'assets/bootstrap/js/popper.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'assets/mdb-blogtemplate/js/mdb.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'assets/default/js/script.js' %}"></script>
</head>
<style>
    main {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: auto;
    }
    .file-container {
        width: 100%;
        height: calc(100vh - 150px); /* Adjust height for header and footer */
        overflow-y: scroll;
        border: 1px solid #ccc;
        margin-bottom: 20px;
        position: relative; /* Position relative for overlay */
    }
    #file-content {
        display: block;
        margin: 0 auto;
    }
    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0); /* Transparent background */
        z-index: 1000; /* Ensure overlay is on top */
        pointer-events: none; /* Allow clicks to pass through to underlying elements */
    }
    #intro {
        margin-top: 58px;
    }

    .modal {
            display: none; 
            position: fixed; 
            z-index: 1; 
            left: 0;
            top: 0;
            width: 100%; 
            height: 100%; 
            overflow: auto; 
            background-color: rgb(0,0,0); 
            background-color: rgba(0,0,0,0.4); 
            justify-content: center;
            align-items: center;
        }

        .modal-content {
            background-color: #fefefe;
            margin: auto;
            padding: 20px;
            border: 1px solid #888;
            width: 100%;
            max-width: 4000px;
            height: 90%;
            text-align: center;
        }

        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }

        .close:hover,
        .close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }

        .modal-message {
            font-size: 2.5em;
            font-weight: bold;
        }
    
    @media (max-width: 991px) {
        #intro {
            margin-top: 45px;
        }
    }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const url = '{{ file_url }}';
        const extension = url.split('.').pop().toLowerCase();
        const fileContainer = document.getElementById('file-content');

        if (['png', 'jpg', 'jpeg', 'gif'].includes(extension)) {
            const img = document.createElement('img');
            img.src = url;
            img.classList.add('img-fluid');
            fileContainer.appendChild(img);
        } else if (['mp4', 'webm', 'ogg'].includes(extension)) {
            const video = document.createElement('video');
            video.src = url;
            video.controls = true;
            video.classList.add('video-fluid');
            fileContainer.appendChild(video);
        } else if (extension === 'pdf') {
            const pdfjsLib = window['pdfjs-dist/build/pdf'];
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';
            pdfjsLib.getDocument(url).promise.then(function(pdfDoc) {
                pdfDoc.getPage(1).then(function(page) {
                    const scale = 1.5;
                    const viewport = page.getViewport({ scale: scale });
                    const canvas = document.createElement('canvas');
                    const context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
                    const renderContext = {
                        canvasContext: context,
                        viewport: viewport
                    };
                    page.render(renderContext);
                    fileContainer.appendChild(canvas);
                });
            });
        }

        // Full screen toggle function
        function toggleFullScreen() {
            const elem = document.getElementById('file-container');
            if (!document.fullscreenElement) {
                elem.requestFullscreen().catch(err => {
                    alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
                });
            } else {
                document.exitFullscreen();
            }
        }

        // Prevent inspecting elements and right-clicking in full-screen mode
        document.addEventListener('fullscreenchange', function () {
            if (document.fullscreenElement) {
                document.fullscreenElement.addEventListener('contextmenu', function (event) {
                    event.preventDefault();
                });
                document.fullscreenElement.addEventListener('mousedown', function (event) {
                    event.preventDefault();
                });
                document.fullscreenElement.addEventListener('mouseup', function (event) {
                    event.preventDefault();
                });
            }
        });

        // Disable right-click and keyboard shortcuts for inspecting
        document.addEventListener('contextmenu', function(event) {
            event.preventDefault();
        });

        document.addEventListener('keydown', function(event) {
            if (event.key === 'F12' || (event.ctrlKey && event.shiftKey && event.key === 'I') || (event.ctrlKey && event.shiftKey && event.key === 'C') || (event.ctrlKey && event.shiftKey && event.key === 'J') || (event.ctrlKey && event.key === 'U')) {
                event.preventDefault();
            }
        });

        // Prevent selection and copying
        document.addEventListener('selectstart', function(event) {
            event.preventDefault();
        });

        document.addEventListener('copy', function(event) {
            event.preventDefault();
        });
    });

    
</script>
{% endblock headerContent %}

{% block pageContent %}
<div>
    <p>This content is protected from screenshots.</p>
</div>

<!-- The Modal -->
<div id="myModal" class="modal">
    <div class="modal-content">
        <span class="close" onclick="closeModal()">&times;</span>
        <p class="modal-message">Screenshotting is disabled!</p>
    </div>
</div>
<nav class="navbar navbar-expand-lg navbar-light bg-white fixed-top shadow border-bottom">
    <div class="container">
        <!-- Navbar brand -->
        <a class="navbar-brand" target="_blank" href="">
            <img src="{{ MEDIA_URL }}/default/fms-logo.png" height="16" alt="{{ MEDIA_URL }}" loading="lazy" style="margin-top: -3px;" />
        </a>
        <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarExample01" aria-controls="navbarExample01" aria-expanded="false" aria-label="Toggle navigation">
            <i class="fas fa-bars"></i>
        </button>
    </div>
</nav>

<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card card-default border rounded-0">
            <div class="card-header">
                <h5 class="card-title"><b>Shared Document</b></h5>
            </div>
            <div class="card-body">
                <div class="container-fluid">
                    <div class="row mb-3">
                        <div class="col">
                            <dl>
                                <dt class="text-muted"><b>Title:</b></dt>
                                <dd class="ps-4">{{ post.title }}</dd>
                                <dt class="text-muted"><b>Description:</b></dt>
                                <dd class="ps-4">{{ post.description }}</dd>
                                <dt class="text-muted"><b>Uploaded By:</b></dt>
                                <dd class="ps-4">{{ post.user.username }}</dd>
                                <dt class="text-muted"><b>Filename:</b></dt>
                                <dd class="ps-4">{{ post.file_path|replaceBlank:'uploads/' }}</dd>
                            </dl>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <div class="file-container" id="file-container">
                                <div id="file-content"></div>
                                <div class="overlay"></div>
                            </div>
                        </div>
                    </div>
                  
                </div>
            </div>
        </div>
    </div>
</div>
<script>
    $(function() {
        $('#topNav .nav-link').each(function() {
            var current = '{{ request.get_full_path | urlencode }}'
            if (current == $(this).attr('href')) {
                $(this).parent().addClass('active')
            }
        })
    })
</script>
<script>
    // Detect Print Screen key press and show an alert
document.addEventListener('keydown', function(event) {
    if (event.key === 'PrintScreen') {
        alert('Screenshots are disabled on this page.');
        event.preventDefault();
    }
});

// Detect common screenshot key combinations (e.g., Windows + Shift + S)
document.addEventListener('keydown', function(event) {
    if ((event.ctrlKey && event.key === 's') || (event.ctrlKey && event.key === 'S') || (event.metaKey && event.key === 's') || (event.metaKey && event.key === 'S')) {
        alert('Screenshots are disabled on this page.');
        event.preventDefault();
    }
});

// Detect context menu opening and prevent it
document.addEventListener('contextmenu', function(event) {
    event.preventDefault();
    alert('Right-click is disabled on this page.');
});

// Hide content on focus loss (e.g., user switching to another window or using a screenshot tool)
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') {
        document.body.style.display = 'none';
    } else {
        document.body.style.display = 'block';
    }
});

</script>
<script>
document.addEventListener('keydown', function(e) {
            if (e.key === 'PrintScreen') {
                showModal();
                e.preventDefault();
            }
        });

        document.addEventListener('keyup', function(e) {
            if (e.key === 'PrintScreen') {
                showModal();
                e.preventDefault();
            }
        });

        function showModal() {
            var modal = document.getElementById("myModal");
            modal.style.display = "flex";
        }

        function closeModal() {
            var modal = document.getElementById("myModal");
            modal.style.display = "none";
        }
</script>

{% endblock pageContent %}
