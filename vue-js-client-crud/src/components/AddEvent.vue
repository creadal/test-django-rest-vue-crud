<template>
  <div class="submit-form">
    <div v-if="!submitted">
      <div class="form-group">
        <label for="title">Название</label>
        <input
          type="text"
          class="form-control"
          id="title"
          required
          v-model="event.title"
          name="title"
        />
      </div>

      <div class="form-group">
        <label for="description">Описание</label>
        <input
          class="form-control"
          id="description"
          required
          v-model="event.description"
          name="description"
        />
      </div>
      
      <div class="form-group">
        <label for="date">Дата</label>
        <input
          type="datetime-local"
          class="form-control"
          id="date"
          required
          v-model="event.date"
          name="date"
        />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input
          class="form-control"
          id="email"
          required
          v-model="event.email"
          name="email"
        />
      </div>

      <button @click="saveEvent" class="btn btn-success">Готово</button>
    </div>

    <div v-else>
      <h4>Событие успешно создано!</h4>
      <button class="btn btn-success" @click="newEvent">Еще</button>
    </div>
  </div>
</template>

<script>
import EventDataService from "../services/EventDataService";

export default {
  name: "add-event",
  data() {
    return {
      event: {
        id: null,
        title: "",
        description: "",
        date: null
      },
      submitted: false
    };
  },
  methods: {
    saveEvent() {
      var data = {
        title: this.event.title,
        description: this.event.description,
        date: this.event.date,
        email: this.event.email
      };

      EventDataService.create(data)
        .then(response => {
          this.event.id = response.data.id;
          console.log(response.data);
          this.submitted = true;
        })
        .catch(e => {
          console.log(e);
        });
    },
    
    newEvent() {
      this.submitted = false;
      this.event = {};
    }
  }
};
</script>

<style>
.submit-form {
  max-width: 300px;
  margin: auto;
}
</style>