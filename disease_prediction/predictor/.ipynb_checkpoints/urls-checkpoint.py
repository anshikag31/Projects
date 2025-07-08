{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "751f6047-4876-42ab-83cd-708df32bd2f5",
   "metadata": {},
   "outputs": [],
   "source": [
    "from django.urls import path\n",
    "from .views import predict_disease  # Ensure you import the correct function from views.py\n",
    "\n",
    "urlpatterns = [\n",
    "    path('predict/', predict_disease, name='predict'),\n",
    "]"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
