<?php
  $counterFile = 'counter.txt';
  if (!file_exists($counterFile)) {
    file_put_contents($counterFile, '0');
  }
  $counter = (int)file_get_contents($counterFile);
  $counter++;
  file_put_contents($counterFile, $counter);
  echo $counter;
?>
