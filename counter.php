<?php
  // Имя куки для идентификации пользователя
  $cookieName = 'site_visit';

  // Проверяем, установлено ли уже куки
  if (!isset($_COOKIE[$cookieName])) {
    // Если куки не установлено, увеличиваем счетчик и устанавливаем куки
    $counterFile = 'counter.txt';

    // Проверяем существует ли файл счетчика
    if (file_exists($counterFile)) {
      // Если файл существует, читаем значение счетчика
      $counter = (int)file_get_contents($counterFile);
      // Увеличиваем значение счетчика на 1
      $counter++;
    } else {
      // Если файл не существует, создаем новый счетчик и устанавливаем его значение в 1
      $counter = 1;
    }

    // Записываем новое значение счетчика обратно в файл
    file_put_contents($counterFile, $counter);

    // Устанавливаем куки на 24 часа
    setcookie($cookieName, 'visited', time() + (24 * 3600));
  } else {
    // Если куки уже установлено, просто считываем значение счетчика из файла
    $counterFile = 'counter.txt';
    $counter = (int)file_get_contents($counterFile);
  }

  // Выводим значение счетчика на страницу
  echo $counter;
?>
