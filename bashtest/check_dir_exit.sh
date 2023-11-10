if [ -d "a" ]; then
  echo "True"
  rm -r  'a'  
else
  echo "False"
  mkdir 'a'
fi

