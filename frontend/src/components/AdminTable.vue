<!-- <script setup>
    defineProps({
        nm: String,
        hd: String,
        type: String
    })
</script>

<template>
    <div class="p-4">
        <div class="tabnav m-3 d-flex justify-content-between">
            <h2>{{hd}}</h2>
            <button v-if="type==='doc'" class="btn btn-outline-success">Create +</button>
        </div>
        <div class="table-responsive">

            <table class="table table-striped table-hover table-bordered">
                <thead class="table-info">
                    <tr>
                        <th>Name</th>
                        <th class="d-flex justify-content-center">Actions</th>
                    </tr>
                </thead>
                <tbody >
                    <tr>
                        <td>
                            {{nm}}
                        </td>
                        <td>
                            <div class="d-flex justify-content-center gap-4">
                                <button class="btn btn-warning">Edit/View</button>
                                <button class="btn btn-danger">Delete</button>
                                <button class="btn btn-dark">BlackList</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template> -->

<script setup>
defineProps({
    nm: String,
    hd: String,
    type: String
})
</script>

<template>
  <div class="p-4">
    <!-- Header -->
    <div class="tabnav mb-4 d-flex justify-content-between align-items-center">
      <h2 class="mb-0">{{ hd }}</h2>
      <button v-if="type === 'doc'" class="btn btn-success">
        <i class="bi bi-plus-lg"></i> Create
      </button>
    </div>

    <!-- Table -->
    <div class="table-responsive shadow-sm rounded">
      <table class="table table-striped table-hover table-bordered align-middle mb-0">
        <thead class="table-info text-center text-uppercase">
          <tr>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ nm }}</td>
            <td>
              <div class="d-flex justify-content-center gap-2">
                <button class="btn btn-sm btn-warning">
                  <i class="bi bi-pencil-fill"></i> Edit
                </button>
                <button class="btn btn-sm btn-danger">
                  <i class="bi bi-trash-fill"></i> Delete
                </button>
                <button class="btn btn-sm btn-dark">
                  <i class="bi bi-slash-circle-fill"></i> Blacklist
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
/* Optional: improve table shadow and rounded corners */
.table-responsive {
  overflow: hidden;
  border-radius: 0.5rem;
}
</style>
