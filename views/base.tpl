% from lib.bottle import template
% setdefault('footer', False)
% setdefault('page', 'index')
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="Отображение данных, получаемых от распределённой сети датчиков">

        <title>Remote Sensors: отображение информации от распределённой сети датчиков</title>

    <!-- Bootstrap core CSS -->
<link href="https://getbootstrap.com/docs/4.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <link href="https://getbootstrap.com/docs/4.3/examples/blog/blog.css" rel="stylesheet">
         <link rel="canonical" href="https://getbootstrap.com/docs/4.3/examples/sticky-footer-navbar/">



    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>
    <!-- Custom styles for this template -->
    <link href="https://getbootstrap.com/docs/4.3/examples/sticky-footer-navbar/sticky-footer-navbar.css" rel="stylesheet">
       <!-- <link href="https://getbootstrap.com/docs/4.3/examples/sign-in/signin.css" rel="stylesheet"> -->
    </head>
    <body class="d-flex flex-column">
        % include('header.tpl', user = user, page = page)
<main role="main" class="flex-shrink-0">
    <div class="container h-100">
        {{!base}}
    </div>
</main>
% if footer:
    % include('footer.tpl')
% end
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script>window.jQuery || document.write('<script src="https://getbootstrap.com/docs/4.3/assets/js/vendor/jquery-slim.min.js"><\/script>')</script><script src="https://getbootstrap.com/docs/4.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-xrRywqdh3PHs8keKZN+8zzc5TX0GRTLCcmivcbNJWm2rs5C8PRhcEn3czEjhAO9o" crossorigin="anonymous"></script>
</body>
</html>