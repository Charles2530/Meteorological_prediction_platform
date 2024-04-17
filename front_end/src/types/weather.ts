export interface WeatherData {
  pid: number;
  city: string;
  temperature: number;
  humidity: number;
  windSpeed: number;
}

export interface NotificationData {
  id: number;
  img: string;
  title: string;
  date: string;
  content: string;
  instruction: string;
}
