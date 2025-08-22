<template lang="html">
    <div id="report-form">
        <div class="row align-items-end mb-5">
            <div class="col-lg-12">
                <h3>Mooring Booking Reports (By Created Date) </h3>
            </div>
            <div class="col-md-2 mb-3">
                <label for="booking_cd_start_date" class="form-label">Start Date</label>
                <input
                    id="booking_cd_start_date"
                    type="date"
                    class="form-control"
                    name="booking_cd_start_date"
                    v-model="booking_cd_start_date"
                    :max="booking_cd_end_date"
                />
            </div>
            <div class="col-md-2 mb-3">
                <label for="booking_cd_end_date" class="form-label">End Date</label>
                <input
                    id="booking_cd_end_date"
                    type="date"
                    class="form-control"
                    name="booking_cd_end_date"
                    v-model="booking_cd_end_date"
                    :min="booking_cd_start_date"
                />
            </div>
            <div class="col-md-3 mb-3">
                <button @click.prevent="generateBookingCDReport()" class="btn btn-primary pull-left" >Generate Reports</button>
            </div>
        </div>

        <div class="row align-items-end mb-5">
            <div class="col-lg-12">
                <h3>Admission Booking Report (By Created Date) </h3>
            </div>
            <div class="col-md-2 mb-3">
                <label for="booking_admission_cd_start_date">Start Date</label>
                <input
                    id="booking_admission_cd_start_date"
                    type="date"
                    class="form-control"
                    name="booking_admission_cd_start_date"
                    v-model="booking_admission_cd_start_date"
                    :max="booking_admission_cd_end_date"
                />
            </div>
            <div class="col-md-2 mb-3">
                <label for="booking_admission_cd_end_date">End Date</label>
                <input
                    id="booking_admission_cd_end_date"
                    type="date"
                    class="form-control"
                    name="booking_admission_cd_end_date"
                    v-model="booking_admission_cd_end_date"
                    :min="booking_admission_cd_start_date"
                />
            </div>
            <div class="col-md-3 mb-3">
                <button @click.prevent="generateBookingCDAdmissionReport()" class="btn btn-primary pull-left" >Generate Reports</button>
            </div>
        </div>

        <div class="row align-items-end">
            <div class="col-lg-12">
                <h3>Mooring Booking Reports (By Departure Date) </h3>
            </div>
            <div class="col-md-2 mb-3">
                <label for="booking_departure_cd_start_date">Start Date</label>
                <input
                    id="booking_departure_cd_start_date"
                    type="date"
                    class="form-control"
                    name="booking_departure_cd_start_date"
                    v-model="booking_departure_cd_start_date"
                    :max="booking_departure_cd_end_date"
                />
            </div>
            <div class="col-md-2 mb-3">
                <label for="booking_departure_cd_end_date">End Date</label>
                <input
                    id="booking_departure_cd_end_date"
                    type="date"
                    class="form-control"
                    name="booking_departure_cd_end_date"
                    v-model="booking_departure_cd_end_date"
                    :min="booking_departure_cd_start_date"
                />
            </div>
            <div class="col-md-3 mb-3">
                <button @click.prevent="generateBookingDepartureReport()" class="btn btn-primary pull-left" >Generate Reports</button>
            </div>
        </div>
    </div>
</template>

<script>
import { api_endpoints, Moment } from "../../hooks.js"
export default {
    name:"reports",
    data:function () {
        let vm = this;
        return {
            booking_cd_start_date: '', // e.g., '2025-10-20'
            booking_cd_end_date: '',   // e.g., '2025-10-30'
            booking_admission_cd_start_date: '',
            booking_admission_cd_end_date: '',
            booking_departure_cd_start_date: '',
            booking_departure_cd_end_date: '',
        };
    },
    watch:{
        // These watchers prevent invalid date ranges that can occur from manual input
        // or by changing one date to conflict with the other.
        booking_cd_start_date(newStartDate) {
            // If the user selects a start date that is after the current end date,
            // reset the end date to prevent an invalid state.
            if (newStartDate && this.booking_cd_end_date && newStartDate > this.booking_cd_end_date) {
                this.booking_cd_end_date = '';
            }
        },
        booking_cd_end_date(newEndDate) {
            if (newEndDate && this.booking_cd_start_date && newEndDate < this.booking_cd_start_date) {
                this.booking_cd_start_date = '';
            }
        },
        booking_admission_cd_start_date(newStartDate) {
            if (newStartDate && this.booking_admission_cd_end_date && newStartDate > this.booking_admission_cd_end_date) {
                this.booking_admission_cd_end_date = '';
            }
        },
        booking_admission_cd_end_date(newEndDate) {
            if (newEndDate && this.booking_admission_cd_start_date && newEndDate < this.booking_admission_cd_start_date) {
                this.booking_admission_cd_start_date = '';
            }
        },
        booking_departure_cd_start_date(newStartDate) {
            if (newStartDate && this.booking_departure_cd_end_date && newStartDate > this.booking_departure_cd_end_date) {
                this.booking_departure_cd_end_date = '';
            }
        },
        booking_departure_cd_end_date(newEndDate) {
            if (newEndDate && this.booking_departure_cd_start_date && newEndDate < this.booking_departure_cd_start_date) {
                this.booking_departure_cd_start_date = '';
            }
        }
    },
    methods:{
        generateBookingCDReport: function () {
            // The date values are now directly available on 'this' in YYYY-MM-DD format.
            const startDate = this.booking_cd_start_date;
            const endDate = this.booking_cd_end_date;

            if (!startDate || !endDate) {
                swal.fire('Error', 'Please select both a start and end date.', 'error');
                console.error("Please select both a start and end date.");
                return; // Stop the function if dates are missing.
            }

            // We need to convert the dates from YYYY-MM-DD (from data) to DD/MM/YYYY for the API.
            const values = {
                "start": Moment(startDate, 'YYYY-MM-DD').format('DD/MM/YYYY'),
                "end": Moment(endDate, 'YYYY-MM-DD').format('DD/MM/YYYY'),
            };
            
            // Build the URL.
            const queryParams = new URLSearchParams(values).toString();
            const url = `${api_endpoints.bookings_created_report}?${queryParams}`;

            // Redirect the user to the report URL.
            window.location.assign(url);
        },
        generateBookingCDAdmissionReport: function () {
            const startDate = this.booking_admission_cd_start_date;
            const endDate = this.booking_admission_cd_end_date;

            if (!startDate || !endDate) {
                swal.fire('Error', 'Please select both a start and end date.', 'error');
                console.error("Please select both a start and end date.");
                return; // Stop the function if dates are missing.
            }

            const values = {
                "start": Moment(startDate, 'YYYY-MM-DD').format('DD/MM/YYYY'),
                "end": Moment(endDate, 'YYYY-MM-DD').format('DD/MM/YYYY'),
            };

            const queryParams = new URLSearchParams(values).toString();
            const url = `${api_endpoints.bookings_admission_created_report}?${queryParams}`;

            window.location.assign(url);
        },
        generateBookingDepartureReport: function () {
            const startDate = this.booking_departure_cd_start_date;
            const endDate = this.booking_departure_cd_end_date;

            if (!startDate || !endDate) {
                swal.fire('Error', 'Please select both a start and end date.', 'error');
                console.error("Please select both a start and end date.");
                return; // Stop the function if dates are missing.
            }

            const values = {
                "start": Moment(startDate, 'YYYY-MM-DD').format('DD/MM/YYYY'),
                "end": Moment(endDate, 'YYYY-MM-DD').format('DD/MM/YYYY'),
            };

            const queryParams = new URLSearchParams(values).toString();
            const url = `${api_endpoints.bookings_departure_report}?${queryParams}`;

            window.location.assign(url);
        },
    },
}

</script>

<style lang="css">
</style>
