<template>
  <div class="list row">
    <div class="col-md-8">
      <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder="Искать по названию"
          v-model="title"/>
        <div class="input-group-append">
          <button class="btn btn-outline-secondary" type="button"
            @click="searchTitle"
          >
            Искать
          </button>
        </div>
      </div>
        <div>
            <input name="datefilter" type="radio" id="all" value="all" checked="checked" v-model="datefilter">
            <label for="all">Все</label>
            <br>
            <input name="datefilter" type="radio" id="day" value="day" v-model="datefilter">
            <label for="day">За последний день</label>
            <br>
            <input name="datefilter" type="radio" id="week" value="week" v-model="datefilter">
            <label for="week">За последнюю неделю</label>
            <br>
            <input name="datefilter" type="radio" id="month" value="month" v-model="datefilter">
            <label for="month">За последний месяц</label>
            <br>
            <button class="btn btn-outline-secondary" type="button"
            @click="filterDate"
            > 
            Отфильтровать
          </button>
        </div>
    </div>
    <div class="col-md-6">
      <h4>События</h4>
      <ul class="list-group">
        <li class="list-group-item"
          :class="{ active: index == currentIndex }"
          v-for="(event, index) in events"
          :key="index"
          @click="setActiveEvent(event, index)"
        >
          {{ event.title }}
        </li>
      </ul>

      <button class="m-3 btn btn-danger" @click="removeAllEvents">
        Удалить все
      </button>
    </div>
    <div class="col-md-6">
      <div v-if="currentEvent">
        <h4>Детали</h4>
        <div>
          <label><strong>Название:</strong></label> {{ currentEvent.title }}
        </div>
        <div>
          <label><strong>Описание:</strong></label> {{ currentEvent.description }}
        </div>
        <div>
          <label><strong>Дата и время проведения:</strong></label> {{ currentEvent.date | moment('timezone', 'UTC', 'DD.MM.YYYY HH:mm') }}
        </div>

        <a class="badge badge-warning"
          :href="'/events/' + currentEvent.id"
        >
          Редактировать
        </a>
      </div>
      <div v-else>
        <br />
        <p>Выберите событие...</p>
      </div>
    </div>
  </div>
</template>

<script>
import EventDataService from "../services/EventDataService";

export default {
  name: "events-list",
  data() {
    return {
      events: [],
      currentEvent: null,
      currentIndex: -1,
      title: ""
    };
  },
  methods: {
    retrieveEvents() {
      EventDataService.getAll()
        .then(response => {
          this.events = response.data;
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
    },

    refreshList() {
      this.retrieveEvents();
      this.currentEvent = null;
      this.currentIndex = -1;
    },

    setActiveEvent(event, index) {
      this.currentEvent = event;
      this.currentIndex = index;
    },

    removeAllEvents() {
      EventDataService.deleteAll()
        .then(response => {
          console.log(response.data);
          this.refreshList();
        })
        .catch(e => {
          console.log(e);
        });
    },
    
    searchTitle() {
      EventDataService.findByTitle(this.title)
        .then(response => {
          this.events = response.data;
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
    },

    filterDate() {
      EventDataService.filterByDate(this.datefilter)
        .then(response => {
          this.events = response.data;
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
    }
  },
  mounted() {
    this.retrieveEvents();
  }
};
</script>

<style>
.list {
  text-align: left;
  max-width: 750px;
  margin: auto;
}
</style>