import { getEntity } from "../../../src/fake_data/entity";

export const createPlantEntities = () => [
  getEntity("plant", "lemon_tree", "ok", {
    problem: "none",
    sensors: {
      moisture: "sensor.lemon_tree_moisture",
      battery: "sensor.lemon_tree_battery",
      temperature: "sensor.lemon_tree_temperature",
      conductivity: "sensor.lemon_tree_conductivity",
      brightness: "sensor.lemon_tree_brightness",
    },
    unit_of_measurement_dict: {
      temperature: "°C",
      moisture: "%",
      brightness: "lx",
      battery: "%",
      conductivity: "μS/cm",
    },
    moisture: 54,
    battery: 95,
    temperature: 15.6,
    conductivity: 1,
    brightness: 12,
    max_brightness: 20,
    friendly_name: "Lemon Tree",
  }),
  getEntity("plant", "apple_tree", "ok", {
    problem: "brightness",
    sensors: {
      moisture: "sensor.apple_tree_moisture",
      battery: "sensor.apple_tree_battery",
      temperature: "sensor.apple_tree_temperature",
      conductivity: "sensor.apple_tree_conductivity",
      brightness: "sensor.apple_tree_brightness",
    },
    unit_of_measurement_dict: {
      temperature: "°C",
      moisture: "%",
      brightness: "lx",
      battery: "%",
      conductivity: "μS/cm",
    },
    moisture: 54,
    battery: 2,
    temperature: 15.6,
    conductivity: 1,
    brightness: 25,
    max_brightness: 20,
    friendly_name: "Apple Tree",
  }),
  getEntity("plant", "sunflowers", "ok", {
    problem: "moisture, temperature, conductivity",
    sensors: {
      moisture: "sensor.sunflowers_moisture",
      temperature: "sensor.sunflowers_temperature",
      conductivity: "sensor.sunflowers_conductivity",
      brightness: "sensor.sunflowers_brightness",
    },
    unit_of_measurement_dict: {
      temperature: "°C",
      moisture: "%",
      brightness: "lx",
      conductivity: "μS/cm",
    },
    moisture: 54,
    temperature: 15.6,
    conductivity: 1,
    brightness: 25,
    entity_picture: "/images/sunflowers.jpg",
  }),
];
