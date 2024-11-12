# Hemse

This project is a frontend for [Visby](https://github.com/klawik-j/visby), designed to display various data related to fitness training. It allows users to view and track their fitness metrics as well as add data, such as weight measurements and different types of activities.

## Instalation
```
pip install hemse
export BACKEND_URL=hosted-visby-app-url
gunicorn hemse.app:server --bind 0.0.0.0:$8000
```

## Examples
![Add weight view](docs/img/view_add_weight.jpg)
![Add activity view](docs/img/view_add_activity.jpg)
![Activity counter](docs/img/view_telemetry_activity_counter.jpg)
![Activity heatmap](docs/img/view_telemetry_heatmap.jpg)
![Activity type pie chart](docs/img/view_telemetry_pie_chart.jpg)
![Weight chart](docs/img/view_telemetry_chart.jpg)

## Contact
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin&logoColor=white&style=flat-square)](https://www.linkedin.com/in/klawikowski-jakub)
[![Email](https://img.shields.io/badge/Email-Contact%20Me-blue?logo=gmail&logoColor=white&style=flat-square)](mailto:klawik.j@gmail.com)
