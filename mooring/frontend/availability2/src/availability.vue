<template>
    <div id="sites-cal" ref="availabilityWrapper">
        <div class="container">
            <a name="makebooking" />
            <div class="row" v-if="status == 'offline'">
                <div class="col-12">
                    <div class="alert alert-danger" role="alert">
                        Sorry, this mooring doesn't yet support online bookings. Please visit the <a href="">Mooring Availability checker</a> for expected availability.
                    </div>
                </div>
            </div>
            <div class="row" v-else-if="status == 'empty'">
                <div class="col-12">
                    <div class="alert alert-danger" role="alert">
                        Sorry, this mooring doesn't yet have any mooring assigned to it. Please visit the <a href="">Mooring Availability checker</a> for expected availability.
                    </div>
                </div>
            </div>
            <div class="row" v-else-if="status == 'closed'">
                <div class="col-12">
                    <div class="alert alert-danger" role="alert">
                        Sorry, this mooring is closed for the selected period. Please visit the <a href="">Mooring Availability checker</a> for expected availability.
                    </div>
                </div>
            </div>
            <div class="row" v-if="errorMsg">
                <div class="col-12">
                    <div class="alert alert-danger" role="alert">
                        Sorry, there was an error placing the booking: {{ errorMsg }} <br/>
                        <template v-if="showSecondErrorLine">
                        Please try again later. If this reoccurs, please contact <a href="">Parks and Visitor Services</a> with this error message, the mooring and the time of the request.
                        </template>
                    </div>
                </div>
            </div>
            <div class="row" v-if="timeleft < 0">
                <div class="col-12">
                    <div class="alert alert-danger" role="alert">
                        Session Expired <br/>
                        <template v-if="showSecondErrorLine">
                        Sorry your Session has expired
                        </template>
                    </div>
                </div>
            </div>

            <!-- A single row for the entire trolley section -->
            <div class="row mb-3">
                <div class="col-12">
                    <div class="card">
                        <!-- Card Header now contains Title, Timer, and Cancel button -->
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0">Trolley: <span id='total_trolley'>${{ total_booking }}</span></h5>
                            
                            <div v-show="ongoing_booking" class="d-flex align-items-center">
                                <!-- Timer Text (using Badge for styling) -->
                                <!-- <span class="badge bg-warning text-dark me-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clock me-1" viewBox="0 0 16 16"><path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71z"/><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0"/></svg>
                                    Time Left: {{ timeleft }}
                                </span> -->
                                <!-- <span class="text-warning-emphasis d-flex align-items-center me-3"> -->
                                <span class="text-danger-emphasis d-flex align-items-center me-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clock-fill me-1" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/></svg>
                                    Time Left: <strong class="ms-1">{{ timeleft }}</strong>
                                </span>
                                
                                <!-- Cancel Button -->
                                <a v-if="current_booking.length > 0" :href="parkstayUrl+'/booking/abort'" class="btn btn-sm btn-warning">Cancel in-progress booking</a>
                            </div>
                        </div>
                        
                        <!-- List Group for the items -->
                        <ul class="list-group list-group-flush" v-if="current_booking.length > 0">
                            <li v-for="item in current_booking" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
                                <span>{{ item.item }}</span>
                                <div class="d-flex align-items-center">
                                    <span class="me-3">${{ item.amount }}</span>
                                    <!-- <button v-show="item.past_booking == false" type="button" class="btn-close" @click="deleteBooking(item.id, item.past_booking)" aria-label="Remove item"></button> -->
                                     <a href="#" v-show="item.past_booking == false" @click.prevent="deleteBooking(item.id, item.past_booking)" class="text-danger" title="Remove item">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
    </svg>
</a>
                                </div>
                            </li>
                        </ul>

                        <!-- Card Body (or Footer) for the Checkout Button -->
                        <div class="card-body text-end">
                            <div v-if="vesselRego.length < 0.1 || vesselRego == ' ' || vesselSize < 0.1 || vesselDraft < 0.1">
                                <button title="Please enter vessel details" class="btn btn-primary" @click="validateVessel()">Proceed to Check Out</button>
                            </div>
                            <div v-else>
                               <div v-if="vesselWeight == 0 && vesselBeam == 0">
                                <button title="Please enter vessel details" class="btn btn-primary" @click="validateVessel()">Proceed to Check Out</button>
                               </div>
                               <div v-else>
                                <a v-if="current_booking.length > 0 && booking_changed == true && numAdults >= 0" class="btn btn-primary" :href="parkstayUrl+'/booking'">Proceed to Check Out</a>
                                <button v-else-if="current_booking.length > 0 && booking_changed == true && numAdults < 0" class="btn btn-secondary" disabled>Please select minimum of 1 adult guest</button>
                                <button v-else class="btn btn-secondary" disabled>Add items to Proceed to Check Out</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <loader :isLoading.sync="isLoading">&nbsp;</loader>

            <div class="row mt-4" v-if="name">
                <div class="col-12">
                    <h4>Book mooring:</h4>
                </div>
            </div>

            <!-- This section is hidden, but we'll style it with BS5 just in case -->
            <div v-if="ongoing_booking" class="row d-none">
                <div class="col-12">
                    <div class="d-flex justify-content-between align-items-center">
                        <span>{{ timeleft }}</span>
                        <div>
                            <a :href="parkstayUrl+'/booking'" class="btn btn-warning">
                                Complete in-progress booking
                            </a>
                            <template v-if="parseInt(parkstayGroundRatisId) > 0">
                                <a :href="parkstayUrl+'/booking/abort?change=true&change_ratis='+parkstayGroundRatisId" class="btn btn-warning ms-2">
                                    Cancel in-progress booking
                                </a>
                            </template>
                            <template v-else>
                                <a :href="parkstayUrl+'/booking/abort?change=true&change_id='+parkstayGroundId" class="btn btn-warning ms-2">
                                    Cancel in-progress booking
                                </a>
                            </template>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mb-2" v-show="status == 'online'">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <!-- A new row for the form controls INSIDE the card -->
                            <div class="row g-3">
                                <!-- This section is hidden, but styled with BS5 -->
                                <div v-if="long_description" class="col-12 d-none">
                                    <div class="mb-3">
                                        <button type="button" class="btn btn-outline-secondary" @click="toggleMoreInfo">
                                            More Information
                                            <i v-if="!showMoreInfo" class="fa fa-caret-down ms-2"></i>
                                            <i v-else class="fa fa-caret-up ms-2"></i>
                                        </button>
                                    </div>
                                    <div class="mb-3" v-if="showMoreInfo">
                                        <div v-html="long_description"></div>
                                    </div>
                                </div>
                                <div class="col-sm-6 col-lg-2">
                                    <label for="date-arrival" class="form-label">Arrival</label>
                                    <input
                                        id="date-arrival"
                                        type="date"
                                        class="form-control"
                                        placeholder="dd/mm/yyyy"
                                        @change="update"
                                        v-model="arrivalDateFormatted"
                                        :max="departureDateFormatted"
                                    />
                                </div>
                                <div class="col-sm-6 col-lg-2">
                                    <label for="date-departure" class="form-label">Departure</label>
                                    <input
                                        id="date-departure"
                                        type="date"
                                        class="form-control"
                                        placeholder="dd/mm/yyyy"
                                        @change="update"
                                        v-model="departureDateFormatted"
                                        :min="arrivalDateFormatted"
                                    />
                                </div>
                                <!-- Vessel Details Dropdown -->
                                <div class="col-sm-6 col-lg-2">
                                    <label for="vesselDetailsDropdown" class="form-label">Vessel Details</label>
                                    <div class="dropdown">
                                        <button class="btn btn-outline-secondary dropdown-toggle w-100" type="button" id="vesselDetailsDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                                            Details
                                        </button>
                                        <div class="dropdown-menu p-3" aria-labelledby="vesselDetailsDropdown" style="width: 300px;">
                                            <!-- Vessel Rego -->
                                            <div class="row g-3 align-items-center mb-2">
                                                <div class="col-6">
                                                    <label for="vesselRego" class="col-form-label">Vessel Rego</label>
                                                </div>
                                                <div class="col-6">
                                                    <input type="text" id="vesselRego" ref="vesselRego" name="vessel_rego" class="form-control form-control-sm" @blur="searchRego()" v-model="vesselRego" :disabled="current_booking.length > 0">
                                                </div>
                                            </div>
                                            <!-- Vessel Size -->
                                            <div class="row g-3 align-items-center mb-2">
                                                <div class="col-6">
                                                    <label for="vesselSize" class="col-form-label">Vessel Size (Meters)</label>
                                                </div>
                                                <div class="col-6">
                                                    <input type="number" id="vesselSize" ref="vesselSize" name="vessel_size" class="form-control form-control-sm" @change="checkDetails(false)" @blur="checkDetails(false)" v-model="vesselSize" step="0.01" :disabled="current_booking.length > 0">
                                                </div>
                                            </div>
                                            <!-- Vessel Draft -->
                                            <div class="row g-3 align-items-center mb-2">
                                                <div class="col-6">
                                                    <label for="vesselDraft" class="col-form-label">Vessel Draft (Meters)</label>
                                                </div>
                                                <div class="col-6">
                                                    <input type="number" id="vesselDraft" ref="vesselDraft" name="vessel_draft" class="form-control form-control-sm" @change="checkDetails(false)" @blur="checkDetails(false)" v-model="vesselDraft" step="0.01" :disabled="current_booking.length > 0">
                                                </div>
                                            </div>
                                            <!-- Vessel Beam -->
                                            <div class="row g-3 align-items-center mb-2">
                                                <div class="col-6">
                                                    <label for="vesselBeam" class="col-form-label">Vessel Beam (Meters)</label>
                                                </div>
                                                <div class="col-6">
                                                    <input type="number" id="vesselBeam" ref="vesselBeam" name="vessel_beam" class="form-control form-control-sm" @change="checkDetails(false)" @blur="checkDetails(false)" v-model="vesselBeam" step="0.01" :disabled="current_booking.length > 0">
                                                </div>
                                            </div>
                                            <!-- Vessel Weight -->
                                            <div class="row g-3 align-items-center">
                                                <div class="col-6">
                                                    <label for="vesselWeight" class="col-form-label">Vessel Weight (Tonnes)</label>
                                                </div>
                                                <div class="col-6">
                                                    <input type="number" id="vesselWeight" ref="vesselWeight" name="vessel_weight" class="form-control form-control-sm" @change="checkDetails(false)" @blur="checkDetails(false)" v-model="vesselWeight" step="0.01" :disabled="current_booking.length > 0">
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <!-- Guests Dropdown -->
                                <div class="col-sm-6 col-lg-2">
                                    <label for="guestsDropdown" class="form-label">Guests</label>
                                    <div class="dropdown">
                                        <button class="btn btn-outline-secondary dropdown-toggle w-100" type="button" id="guestsDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                                            {{ numPeople }}
                                        </button>
                                        <div class="dropdown-menu p-3" aria-labelledby="guestsDropdown" style="width: 300px;">
                                            <!-- Adults -->
                                            <div class="row g-3 align-items-center mb-2">
                                                <div class="col-6">
                                                    <label for="numAdults" class="col-form-label">Adults</label>
                                                </div>
                                                <div class="col-6">
                                                    <input type="number" id="numAdults" name="num_adults" class="form-control form-control-sm" @change="checkGuests()" v-model="numAdults" min="0" max="16">
                                                </div>
                                            </div>

                                            <!-- Concessions (Hidden) -->
                                            <div class="row g-3 align-items-center mb-2 d-none">
                                                <div class="col-6">
                                                    <label for="numConcessions" class="col-form-label">
                                                        <span title="Holders of one of the following Australian-issued cards: - Seniors Card - Age Pension - Disability Support - Carer Payment - Carer Allowance - Companion Card - Department of Veterans' Affairs">Concessions</span>
                                                    </label>
                                                </div>
                                                <div class="col-6">
                                                    <input type="number" id="numConcessions" name="num_concessions" class="form-control form-control-sm" @change="checkGuests()" v-model="numConcessions" min="0" max="16">
                                                </div>
                                            </div>

                                            <!-- Children -->
                                            <div class="row g-3 align-items-center mb-2">
                                                <div class="col-6">
                                                    <label for="numChildren" class="col-form-label">Children (4-16)</label>
                                                </div>
                                                <div class="col-6">
                                                    <input type="number" id="numChildren" name="num_children" class="form-control form-control-sm" @change="checkGuests()" v-model="numChildren" min="0" max="16">
                                                </div>
                                            </div>

                                            <!-- Infants -->
                                            <div class="row g-3 align-items-center">
                                                <div class="col-6">
                                                    <label for="numInfants" class="col-form-label">Infants (under 4)</label>
                                                </div>
                                                <div class="col-6">
                                                    <input type="number" id="numInfants" name="num_infants" class="form-control form-control-sm" @change="checkGuests()" v-model="numInfants" min="0" max="16">
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-6 col-lg-2">
                                    <label for="distanceRadius" class="form-label" title="Distance to search from the original selected mooring.">Distance (KMs)</label>
                                    <input id="distanceRadius" type="number" class="form-control" placeholder="0" @change="update" v-model="distanceRadius"/>
                                </div>
                                <div class="col-sm-6 col-lg-2">
                                    <!-- A spacer label to align the button vertically with the input field -->
                                    <label class="form-label">&nbsp;</label>
                                    <a :href="'/map/'" class="btn btn-outline-secondary w-100">Search Other Mooring</a>
                                </div>
                                <div v-if="!useAdminApi" class="col-sm-6 col-lg-3 d-none">
                                    <label for="gear_type_select" class="form-label">Equipment</label>
                                    <select id="gear_type_select" name="gear_type" class="form-select" v-model="gearType" @change="update()">
                                        <option value="tent" v-if="gearTotals.tent">Tent</option>
                                        <option value="campervan" v-if="gearTotals.campervan">Campervan</option>
                                        <option value="caravan" v-if="gearTotals.caravan">Caravan / Camper trailer</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row" v-show="status == 'online'">
                <div class="col-12">
                    <div v-if="vesselSize > 0 && vesselDraft > 0">
                        <div v-if="vesselDraft != 0 && vesselWeight != 0">
                            <div class="table-responsive">
                                <table class="table table-bordered table-striped table-hover">
                                    <thead>
                                        <tr>
                                            <th class="site">
                                                <div class="d-flex justify-content-between align-items-center">
                                                    <span>Mooring</span>
                                                    <a class="btn btn-sm btn-outline-secondary d-none" target="_blank" :href="map" v-if="map">View Map</a>
                                                </div>
                                            </th>
                                            <th class="book">Book</th>
                                            <th class="date" v-for="i in days">{{ getDateString(arrivalDate, i-1) }}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <template v-for="(site, index) in sites" >
                                            <tr v-show="mooring_book_row_display[index] == 'show'" >
                                                <td class="site">
                                                    <div>{{ site.name }} - <span class="text-muted">{{ site.mooring_park }}</span></div>
                                                    <small class="text-muted" v-if="site.distance_from_selection > 1">Distance: {{ site.distance_from_selection }}km</small>
                                                    <small class="text-muted" v-else>Distance: {{ site.distance_from_selection_meters }}m</small>
                                                </td>
                                                <td class="book">
                                                    <template v-if="site.price">
                                                        <button v-if="mooring_book_row[index] == true" :disabled="mooring_book_row_disabled[index] == true" @click="addBookingRow(index)" class="btn btn-sm btn-primary w-100">
                                                            Book now<br/>
                                                            <span class="fw-bold">${{ mooring_book_row_price[index] }}</span>
                                                        </button>
                                                        <button v-else disabled class="btn btn-sm btn-secondary w-100 d-none" title="Please complete your current ongoing booking using the button at the top of the page.">
                                                            Book now<br/>
                                                            <span class="fw-bold">${{ site.price }}</span>
                                                        </button>
                                                    </template>
                                                    <template v-else>
                                                        <button v-if="site.breakdown" class="btn btn-sm btn-warning w-100" @click="toggleBreakdown(site)">Show availability</button>
                                                        <button v-else class="btn btn-sm btn-secondary w-100" disabled>Change dates</button>
                                                    </template>
                                                </td>
                                                <td class="date text-center align-middle" v-for="day in site.availability" :class="{ 'table-success': day[0] }">
                                                    <div v-for="bp in day[1].booking_period" class="mb-1">
                                                        <div v-if="bp.status == 'open'">
                                                            <button
                                                                class="btn btn-sm btn-success w-100"
                                                                @click="addBooking(site.id,site.mooring_id,bp.id,bp.date)"
                                                                v-if="bp.caption.length > 1"
                                                                data-bs-toggle="tooltip"
                                                                :title="bp.caption"
                                                            >
                                                                Book {{ bp.period_name }}
                                                                <span v-if="site.mooring_class == 'small'">${{ bp.small_price }}</span>
                                                                <span v-if="site.mooring_class == 'medium'">${{ bp.medium_price }}</span>
                                                                <span v-if="site.mooring_class == 'large'">${{ bp.large_price }}</span>
                                                            </button>
                                                            <button
                                                                v-else
                                                                class="btn btn-sm btn-success w-100"
                                                                @click="addBooking(site.id,site.mooring_id,bp.id,bp.date)"
                                                            >
                                                                Book {{ bp.period_name }}
                                                                <span v-if="site.mooring_class == 'small'">${{ bp.small_price }}</span>
                                                                <span v-if="site.mooring_class == 'medium'">${{ bp.medium_price }}</span>
                                                                <span v-if="site.mooring_class == 'large'">${{ bp.large_price }}</span>
                                                            </button>
                                                        </div>
                                                        <div v-else-if="bp.status == 'selected'">
                                                            <!-- Wrap button and close icon in a relative position container -->
                                                            <div class="position-relative">
                                                                <button class="btn btn-sm btn-info w-100" @click="deleteBooking(bp.booking_row_id, bp.past_booking)"> 
                                                                    Book {{ bp.period_name }}
                                                                    <span v-if="site.mooring_class == 'small'">${{ bp.small_price }}</span>
                                                                    <span v-if="site.mooring_class == 'medium'">${{ bp.medium_price }}</span>
                                                                    <span v-if="site.mooring_class == 'large'">${{ bp.large_price }} </span>
                                                                </button>
                                                                <!-- Position the close button on top of the main button -->
                                                                <a href="#" v-show="bp.past_booking == false" class="text-danger position-absolute top-0 end-0" style="transform: translate(6px, -6px); z-index: 5;" @click.prevent.stop="deleteBooking(bp.booking_row_id, bp.past_booking)" title="Remove">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                                                                        <circle cx="8" cy="8" r="8" fill="white"/>
                                                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                                                                    </svg>
                                                                </a>
                                                            </div>
                                                        </div>
                                                        <div v-else-if="bp.status == 'perday'">
                                                            <button class="btn btn-sm btn-light w-100" disabled>One Mooring Limit</button>
                                                        </div>
                                                        <div v-else-if="bp.status == 'maxstay'">
                                                            <button class="btn btn-sm btn-light w-100" disabled>Max Stay Limit Reached</button>
                                                        </div>
                                                        <div v-else>
                                                            <button class="btn btn-sm btn-danger w-100 disabled" style="text-decoration: line-through; opacity: 0.65;">{{ bp.period_name }}</button>
                                                        </div>
                                                    </div>
                                                </td>
                                            </tr>
                                            <template v-if="site.showBreakdown">
                                                <tr v-for="line in site.breakdown" :key="line.id" class="breakdown">
                                                    <td class="site">Site: {{ line.name }}</td>
                                                    <td></td>
                                                    <td class="date text-center" v-for="day in line.availability" :class="{ 'table-success': day[0] }">{{ day[1] }}</td>
                                                </tr>
                                            </template>
                                        </template>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-12">
                    <!-- Message for missing beam/weight -->
                    <div v-if="vesselSize > 0 && vesselDraft > 0 && vesselWeight == 0 && vesselBeam == 0">
                        <div class="alert alert-warning" role="alert">
                        Please enter a beam length or weight depending on your mooring type.   
                        </div>
                    </div>

                    <!-- Message for no search results -->
                    <div v-if="sites.length == 0 && isLoading == false">
                        <div class="alert alert-info" role="alert">
                            Sorry we couldn't find any mooring matching the query entered.
                        </div>
                    </div>

                    <!-- Message for max advance booking (hidden) -->
                    <div v-if="max_advance_booking_days > max_advance_booking" class="d-none">
                        <div class="alert alert-warning" role="alert">
                            Advanced booking is limited to {{ max_advance_booking }} day/s.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Dropdown, Tooltip } from 'bootstrap';
import debounce from 'debounce';
import moment from 'moment';
import swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.css';
import loader from './loader.vue';

var nowTemp = new Date();
var now = moment.utc({year: nowTemp.getFullYear(), month: nowTemp.getMonth(), day: nowTemp.getDate(), hour: 1, minute: 0, second: 0}).toDate();

var siteType = {
    NOBOOKINGS: 0,
    ONLINE: 1,
    PHONE: 2,
    OTHER: 3
};

function getQueryParam(name, fallback) {
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)");
    var results = regex.exec(window.location.href);
    if (!results) return fallback;
    if (!results[2]) return fallback;
    return decodeURIComponent(results[2].replace(/\+/g, " "));
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

export default {
    el: '#availability',
    components: {
        loader,
    },
    data: function () {
        return {
            name: '',
            arrivalDate: moment.utc(getQueryParam('arrival', moment.utc(now).format('YYYY/MM/DD')), 'YYYY/MM/DD'),
            departureDate:  moment.utc(getQueryParam('departure', moment.utc(now).add(5, 'days').format('YYYY/MM/DD')), 'YYYY/MM/DD'),
            parkstayUrl: '',
            useAdminApi: window.useAdminApi || false,
            // order of preference:
            // - GET parameter 'site_id'
            // - global JS var 'parkstayGroundId'
            // - '1'
            parkstayGroundId: parseInt(getQueryParam('site_id', window.parkstayGroundId || '1')),
            parkstayGroundRatisId: parseInt(getQueryParam('parkstay_site_id', '0')),
            days: 5,
            numAdults: parseInt(getQueryParam('num_adult', 2)),
            numChildren: parseInt(getQueryParam('num_children', 0)),
            numConcessions: parseInt(getQueryParam('num_concession', 0)),
            numInfants: parseInt(getQueryParam('num_infant', 0)),
            vesselSize: parseFloat(getQueryParam('vessel_size', 0)),
            vesselDraft: parseFloat(getQueryParam('vessel_draft', 0)),
            vesselBeam: parseFloat(getQueryParam('vessel_beam', 0)),
            vesselWeight: parseFloat(getQueryParam('vessel_weight', 0)),
            vesselRego: getQueryParam('vessel_rego', ''),
            searchedRego: getQueryParam('vessel_rego', ''),
            distanceRadius: parseInt(getQueryParam('distance_radius', 100)),
            maxAdults: 30,
            maxChildren: 30,
            gearType: getQueryParam('gear_type', 'tent'),
            mooring_vessel_size: 0,
            max_advance_booking: 0,
            max_advance_booking_days: 0,
            gearTotals: {
                tent: 0,
                campervan: 0,
                caravan: 0
            },
            status: null,
            errorMsg: null,
            classes: {},
            sites: [],
            long_description: '',
            isLoading: false,
            map: null,
            showMoreInfo: false,
            ongoing_booking: false,
            ongoing_booking_id: null,
            current_booking: [],
            booking_changed: true,
            total_booking: '0.00',
            showSecondErrorLine: true,
            timer: -1,
            expiry: null,
            booking_expired_notification: false,
            mooring_book_row: [],
            mooring_book_row_price: [],
            mooring_book_row_disabled: [],
            mooring_book_row_display: [],
            loadingID: 0 
        };
    },
    computed: {
        numPeople: {
            cache: false,
            get: function() {
                var count = parseInt(this.numAdults) + parseInt(this.numConcessions) + parseInt(this.numChildren) + parseInt(this.numInfants);
                if (count === 1) {
                    return count +" person";
                } else {
                    return count + " people";
                }
            }
        },
        arrivalDateString: {
            cache: false,
            get: function() {
                return this.arrivalDate ? moment(this.arrivalDate).format('YYYY/MM/DD') : null;
            }
        },
        departureDateString: {
            cache: false,
            get: function() {
                return this.departureDate ? moment(this.departureDate).format('YYYY/MM/DD') : null;
            }
        },
        arrivalDateFormatted: {
            get() {
                if (!this.arrivalDate) return '';
                const d = new Date(this.arrivalDate);
                const year = d.getFullYear();
                const month = String(d.getMonth() + 1).padStart(2, '0');
                const day = String(d.getDate()).padStart(2, '0');
                return `${year}-${month}-${day}`;
            },
            set(value) {
                // user input is converted back to Date object
                if (!value){
                    if (this.departureDate){
                        this.arrivalDate = this.departureDate
                    } else {
                        this.arrivalDate = new Date()
                    }
                } else {
                    this.arrivalDate = new Date(value);
                }
            }
        },
        departureDateFormatted: {
            get() {
                if (!this.departureDate) return '';
                const d = new Date(this.departureDate);
                const year = d.getFullYear();
                const month = String(d.getMonth() + 1).padStart(2, '0');
                const day = String(d.getDate()).padStart(2, '0');
                return `${year}-${month}-${day}`;
            },
            set(value) {
                // user input is converted back to Date object
                if (!value){
                    if (this.arrivalDate){
                        this.departureDate = this.arrivalDate
                    } else {
                        this.departureDate = new Date()
                    }
                } else {
                    this.departureDate = new Date(value);
                }
            }
        },

        timeleft: {
                cache: false,
                get: function get() {
                    // Minutes and seconds
                    var mins = ~~(this.timer / 60);
                    var secs = this.timer % 60;

                    // Hours, minutes and seconds
                    var hrs = ~~(this.timer / 3600);
                    var mins = ~~((this.timer % 3600) / 60);
                    var secs = this.timer % 60;

                    // Output like "1:01" or "4:03:59" or "123:03:59"
                    var ret = "";

                    if (hrs > 0) {
                        ret += "" + hrs + ":" + (mins < 10 ? "0" : "");
                    }

                    ret += "" + mins + ":" + (secs < 10 ? "0" : "");
                    ret += "" + secs;
                    if (this.ongoing_booking) {
                       
                       if (this.timer < 0) {
                            if (this.booking_expired_notification == false) { 
   		   	   console.log('TIMED OUT');
                           clearInterval(this.timer);
//                         var loc = window.location;
//                         window.location = loc.protocol + '//' + loc.host + loc.pathname;
                           this.bookingExpired();
                           this.booking_expired_notification = true;
			}
		       }
                    }
                    return ret;
                }
        }

    },
    methods: {
        toggleMoreInfo: function(){
            this.showMoreInfo ? this.showMoreInfo = false: this.showMoreInfo = true;
        },
        getDateString: function (date, offset) {
            return moment(date).add(offset, 'days').format('ddd MMM D');
        },
        toggleBreakdown: function (site) {
            if (site.showBreakdown) {
                site.showBreakdown = false;
            } else {
                this.sites.forEach(function(el) {
                    el.showBreakdown = false;
                });
                site.showBreakdown = true;
            }
        },
        
        formatDate: function (dateStr) {
            const date = new Date(dateStr);
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
            const year = date.getFullYear();
            return `${day}/${month}/${year}`;
        },

        bookingExpired: function() {
                swal.fire({
                  title: 'Booking Expired',
                  text: "Please click start again to begin booking again:",
                  type: 'warning',
                  showCancelButton: false,
                  confirmButtonText: 'Start Again',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                    }).then((result) => {
                        if (result.isConfirmed) {
                        const loc = window.location;
                        window.location = `${loc.protocol}//${loc.host}/map/`;
                        }
                    });


	},
        createBookingError: function(message) {
                swal.fire({
                  title: 'Error',
                  text: message,
                  type: 'error',
                  showCancelButton: false,
                  confirmButtonText: 'OK',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                })
                return;
        },
        deleteBooking: function(booking_item_id, past_booking) {
             if (past_booking == true) { 
                swal.fire({
                  title: 'Error',
                  text: "Unable to delete past booking",
                  type: 'warning',
                  showCancelButton: false,
                  confirmButtonText: 'OK',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                })
                return;
	     }


              var vm = this;
              vm.loadingID = vm.loadingID + 1;
              var submitData = {
                  booking_item: booking_item_id,
              };

              $.ajax({
                  loadID: vm.loadingID,
                  url: vm.parkstayUrl + '/api/booking/delete',
                  dataType: 'json',
                  method: 'POST',
                  data: submitData,
                  success: function(data, stat, xhr) {
                     if (data.result == 'error') { 
                         swal.fire({
                            title: 'Error',
                            text: data.message,
                            type: 'warning',
                            showCancelButton: false,
                            confirmButtonText: 'OK',
                            showLoaderOnConfirm: true,
                            allowOutsideClick: false
                         })
                     }


                      vm.update();
                  },
                  error: function(data, stat, err) {
                     swal.fire({
	                  title: 'Error',
        	          text: 'Uknown Error',
                	  type: 'warning',
	                  showCancelButton: false,
        	          confirmButtonText: 'OK',
	                  showLoaderOnConfirm: true,
	                  allowOutsideClick: false
        	        })



                       vm.update();
                  }
              });

	},
	addBookingRow: function(site_index_id) {
                        var vm = this;
                        var avail_index;
                        // vm.sites = data.sites;
                        for (avail_index = 0; avail_index < vm.sites[site_index_id].availability.length; ++avail_index) {
                                        var booking_period = vm.sites[site_index_id].availability[avail_index][1].booking_period;
                                        //if (booking_period.length > 1) {
                                        //        vm.mooring_book_row[index] = false;
                                        //}
                                        vm.addBooking(vm.sites[site_index_id].id, vm.sites[site_index_id].mooring_id, booking_period[0].id, booking_period[0].date);
                                        //if (vm.ongoing_booking == false) {
                                           
                                        //}
                        }


	},
        addBooking: function (site_id, mooring_id,bp_id,date) {
              var vm = this;
              vm.loadingID = vm.loadingID + 1;
              vm.isLoading =true;
              $('#spinnerLoader').show();
              
              var booking_start = vm.formatDate($('#date-arrival').val());
              var booking_finish = vm.formatDate($('#date-departure').val());

              var submitData = {
                  site_id: site_id,
                  mooring_id: mooring_id,
                  bp_id: bp_id,
                  date: date,
                  booking_start: booking_start,
                  booking_finish: booking_finish,
                  num_adult: vm.numAdults,
                  num_children : vm.numChildren,
                  num_infant: vm.numInfants
              };

              $.ajax({
                  loadID: vm.loadingID,
                  url: vm.parkstayUrl + '/api/booking/create', 
                  dataType: 'json',
                  method: 'POST',
                  //async: false,
                  data: submitData, 
                  success: function(data, stat, xhr) {
                     if (this.loadID == vm.loadingID) { 
                         vm.isLoading =false;
                         $('#spinnerLoader').hide();
	             }
                     if (data.result == 'error') { 
                          vm.createBookingError(data.message); 
                     }
                     vm.update();
                  },
                  error: function(xhr, stat, err) {
                       if (this.loadID == vm.loadingID) {
                           vm.isLoading =false;
                           $('#spinnerLoader').hide();
                       }
                       vm.update();
                  }
              });
        },
        submitBooking: function (site) {
            alert('not working yet');
            return;
            var vm = this;
            if (vm.vesselSize > 0 ) { 
            } else {
                swal.fire({
                  title: 'Missing Vessel Size',
                  text: "Please enter vessel size:",
                  type: 'warning',
                  showCancelButton: false,
                  confirmButtonText: 'OK',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                })
                return;
            }

            var submitData = {
                arrival: vm.arrivalDateString,
                departure: vm.departureDateString,
                num_adult: vm.numAdults,
                num_child: vm.numChildren,
                num_concession: vm.numConcessions,
                num_infant: vm.numInfants,
                vessel_size: vm.vesselSize
            };
            if (site.type == 0) { // per site listing
                submitData.campsite = site.id;
            } else {
                submitData.campground = vm.parkstayGroundId;
                submitData.campsite_class = site.type;
            }
            $.ajax({
                url: vm.parkstayUrl + '/api/create_booking',
                method: 'POST',
                data: submitData,
                dataType: 'json',
                crossDomain: true,
                xhrFields: {
                    withCredentials: true
                },
                success: function(data, stat, xhr) {
                    if (data.status == 'success') {
                        window.location.href = vm.parkstayUrl + '/booking';
                    }
                },
                error: function(xhr, stat, err) {
                    console.log('POST error');
                    //console.log(xhr);
                    vm.errorMsg = (xhr.responseJSON && xhr.responseJSON.msg) ? xhr.responseJSON.msg : '"'+err+'" response when communicating with Mooring.';
                    vm.update();
                }
            });
        },
        updateURL: function () {
            // update browser history
            var vm = this;
            var newHist = window.location.href.split('?')[0] +'?'+ $.param({
                site_id: vm.parkstayGroundId,
                arrival: moment(vm.arrivalDate).format('YYYY/MM/DD'),
                departure: moment(vm.departureDate).format('YYYY/MM/DD'),
                gear_type: vm.gearType,
                num_adult: vm.numAdults,
                num_child: vm.numChildren,
                num_concession: vm.numConcessions,
                num_infant: vm.numInfants,
                vessel_size : vm.vesselSize,
                vessel_draft: vm.vesselDraft,
                vessel_beam: vm.vesselBeam,
                vessel_weight: vm.vesselWeight,
                vessel_rego: vm.vesselRego,
            });
            history.replaceState('', '', newHist);
        },
        searchRego: function(rego){
            let vm = this;
            vm.vesselRego = vm.vesselRego.replace(/ /g, "");
            vm.vesselRego = vm.vesselRego.toUpperCase();
            vm.vesselRego = vm.vesselRego.replace(/\s/g,"");
            vm.vesselRego = vm.vesselRego.replace(/\W/g,"");

            if (rego){
                var reg = rego;
            } else {
                var reg = vm.vesselRego
            }
            var not_null = true
            if (reg == null || reg == "" || reg == " "){
                not_null = false;
            }
            var data = {
                'rego': reg
            }
            if(reg && not_null && vm.searchedRego != reg){
                console.log('in searchRego2');
                $.ajax({
                    url: "/api/registeredVessels/",
                    dataType: 'json',
                    data: data,
                    method: 'GET',
                    success: function(data, stat, xhr) {
                        vm.searchedRego = reg;
                        if(data[0]){
                            vm.vesselSize = parseFloat(data[0].vessel_size);
                            vm.vesselWeight = parseFloat(data[0].vessel_weight);
                            vm.vesselDraft = parseFloat(data[0].vessel_draft);
                            vm.vesselBeam = parseFloat(data[0].vessel_beam);  
                        } else {
                            console.log("Registration was not found.");
                        }
                    }
                });
                vm.update();
            }
        },
        checkDetails: function(from_update){
            let vm = this;
            if (vm.vesselSize == null || vm.vesselSize.length == 0){
                console.log("size empty");
                vm.vesselSize = 0;
            }
            if (vm.vesselDraft == null || vm.vesselDraft.length == 0){
                console.log("draft empty");
                vm.vesselDraft = 0;
            }
            if (vm.vesselBeam == null || vm.vesselBeam.length == 0){
                console.log("beam empty");
                vm.vesselBeam = 0;
            } 
            if (vm.vesselWeight == null || vm.vesselWeight.length == 0){
                console.log("weigth empty");
                vm.vesselWeight = 0;
            }
            if (from_update){
                return true;
            } else {
                vm.update();
            }
        },
        checkGuests: function(){
            let vm = this;
            if (vm.numAdults < 0 || vm.numChildren < 0 || vm.numInfants < 0){
                swal.fire({
                    title: 'Invalid Guest Amount',
                    text: "Number of guests cannot be a negative.",
                    type: 'warning',
                    showCancelButton: false,
                    confirmButtonText: 'OK',
                    showLoaderOnConfirm: true,
                    allowOutsideClick: false
                });
                if (vm.numAdults < 1) { 
                   vm.numAdults = 1;
                }
            } else {
                vm.update();
            }
        },
        validateVessel: function(){
            let vm = this;
            if (vm.vesselRego.length < 1 || vm.vesselRego == ' '){
                swal.fire({
                  title: 'Invalid Vessel Registration',
                  text: "Please enter a valid vessel registration",
                  type: 'warning',
                  showCancelButton: false,
                  confirmButtonText: 'OK',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                });
            }
            if (vm.vesselSize < 0.1){
                swal.fire({
                  title: 'Invalid Vessel Size',
                  text: "Please enter a valid vessel size",
                  type: 'warning',
                  showCancelButton: false,
                  confirmButtonText: 'OK',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                });
            }
            if (vm.vesselDraft < 0.1){
                swal.fire({
                  title: 'Invalid Vessel Draft',
                  text: "Please enter a valid vessel draft",
                  type: 'warning',
                  showCancelButton: false,
                  confirmButtonText: 'OK',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                });
            }
            if (vm.vesselBeam < 0.1){
                swal.fire({
                  title: 'Invalid Vessel Beam',
                  text: "Please enter a valid vessel beam",
                  type: 'warning',
                  showCancelButton: false,
                  confirmButtonText: 'OK',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                });
            }
            if (vm.vesselWeight < 0.1){
                swal.fire({
                  title: 'Invalid Vessel Weight',
                  text: "Please enter a valid vessel weight",
                  type: 'warning',
                  showCancelButton: false,
                  confirmButtonText: 'OK',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                });
            }
            if (vm.numAdults < 1){
                swal.fire({
                  title: 'Invalid Number of Adults',
                  text: "Please choose the correct number of adults",
                  type: 'warning',
                  showCancelButton: false,
                  confirmButtonText: 'OK',
                  showLoaderOnConfirm: true,
                  allowOutsideClick: false
                });
            }
        },
        update: function() {
            var vm = this;
            vm.loadingID = vm.loadingID + 1;
            vm.sites = [];
            var ready = vm.checkDetails(true);
            if (ready){
                vm.isLoading =true;
                $('#spinnerLoader').show();
                debounce(function() {
                    var params = {
                        arrival: moment(vm.arrivalDate).format('YYYY/MM/DD'),
                        departure: moment(vm.departureDate).format('YYYY/MM/DD'),
                        num_adult: vm.numAdults,
                        num_child: vm.numChildren,
                        num_concession: vm.numConcessions,
                        num_infant: vm.numInfants,
                        vessel_size: vm.vesselSize,
                        vessel_draft: vm.vesselDraft,
                        vessel_beam: vm.vesselBeam,
                        vessel_weight: vm.vesselWeight,
                        vessel_rego: vm.vesselRego,
                        distance_radius: vm.distanceRadius
                    };
                    if (parseInt(vm.parkstayGroundRatisId) > 0) {
                        var url = vm.parkstayUrl + '/api/availability_ratis/'+ vm.parkstayGroundRatisId +'/?'+$.param(params);
                    } else if (vm.useAdminApi) {
                        var url = vm.parkstayUrl + '/api/availability_admin/'+ vm.parkstayGroundId +'/?'+$.param(params);
                    } else {
                        vm.updateURL();
                        var url = vm.parkstayUrl + '/api/availability2/'+ vm.parkstayGroundId +'.json/?'+$.param(params);
                    }
                    console.log({url})

                    // var options = [null, "", " "]
                    var search = true;
                    // if(options.indexOf(vm.vesselRego) >= 0 || options.indexOf(vm.vesselSize) >= 0 || options.indexOf(vm.vesselDraft) >= 0 || options.indexOf(vm.vesselBeam) >= 0 || options.indexOf(vm.vesselWeight) >= 0){
                    //     search = false;
                    // }
                    if (search){
                        $.ajax({
                            loadID: vm.loadingID,
                            url: url,
                            dataType: 'json',
                            // async: false,
                            success: function(data, stat, xhr) {
                                vm.name = data.name;
                                vm.days = data.days;
                                vm.classes = data.classes;
                                vm.long_description = data.long_description;
                                vm.map = data.map;
                                vm.ongoing_booking = data.ongoing_booking;
                                vm.ongoing_booking_id = data.ongoing_booking_id;
                                vm.mooring_vessel_size = data.vessel_size;
                                vm.max_advance_booking = data.max_advance_booking;
                                vm.max_advance_booking_days = data.max_advance_booking_days;
                                vm.current_booking = data.current_booking;
                                vm.booking_changed = data.booking_changed;
                                vm.total_booking = data.total_booking;
                                vm.timer = data.timer;
                                vm.expiry = data.expiry;
                
                                if (data.error_type != null) {
                                    vm.status = 'online';
                                    return;
                                }

                                if (data.sites == null) { 
                                    return;
                                }

                                if (data.sites.length == 0) {
                                    // vm.status = 'empty';
                                    // return;
                                }

                                vm.gearTotals.tent = 0
                                vm.gearTotals.campervan = 0
                                vm.gearTotals.caravan = 0
                                data.sites.forEach(function(el) {
                                    el.showBreakdown = false;
                                    vm.gearTotals.tent += el.gearType.tent ? 1 : 0;
                                    vm.gearTotals.campervan += el.gearType.campervan ? 1 : 0;
                                    vm.gearTotals.caravan += el.gearType.caravan ? 1 : 0;
                                });
                                if (!vm.gearTotals[vm.gearType]) {
                                    if (vm.gearTotals.tent) {
                                        vm.gearType = 'tent';
                                    } else if (vm.gearTotals.campervan) {
                                        vm.gearType = 'campervan';
                                    } else if (vm.gearTotals.caravan) {
                                        vm.gearType = 'caravan';
                                    } else {
                                        // no campsites at all!
                                        vm.gearType = 'tent';
                                    }
                                }

                                // Booking Whole Row Index
                                var index;
                                var avail_index;
                                var filtered_sites = [];
                                vm.sites = data.sites;
                                vm.mooring_book_row = [];
                                vm.mooring_book_row_disabled = [];
                                vm.mooring_book_row_price = [];
                                vm.mooring_book_row_display = [];

                                for (index = 0; index < vm.sites.length; ++index) {
                                    vm.mooring_book_row[index] = true;
                                    vm.mooring_book_row_disabled[index] = false;
                                    vm.mooring_book_row_price[index] = '0.00';
                                    vm.mooring_book_row_display[index] = 'show';

                                    if (vm.sites[index].vessel_size_limit > 0){
                                        if (vm.sites[index].vessel_size_limit < vm.vesselSize){
                                            if (!filtered_sites.indexOf(vm.sites[index].id) >= 0){
                                            filtered_sites.push(vm.sites[index].id); 
                                            }
                                        }
                                    } 
                                    if (vm.sites[index].vessel_draft_limit > 0){
                                        if (vm.sites[index].vessel_draft_limit < vm.vesselDraft){
                                            if (!filtered_sites.indexOf(vm.sites[index].id) >= 0){
                                            filtered_sites.push(vm.sites[index].id); 
                                            }
                                        }
                                    }
                                    if (vm.sites[index].vessel_beam_limit > 0){
                                        if (vm.sites[index].vessel_beam_limit < vm.vesselBeam){
                                            if (!filtered_sites.indexOf(vm.sites[index].id) >= 0){
                                            filtered_sites.push(vm.sites[index].id); 
                                            }
                                        }
                                    }
                                    if (vm.sites[index].vessel_weight_limit > 0){
                                        if (vm.sites[index].vessel_weight_limit < vm.vesselWeight){
                                            if (!filtered_sites.indexOf(vm.sites[index].id) >= 0){
                                            filtered_sites.push(vm.sites[index].id); 
                                            }
                                        }
                                    }
                                    for (avail_index = 0; avail_index < vm.sites[index].availability.length; ++avail_index) {
                                        var booking_period = vm.sites[index].availability[avail_index][1].booking_period;  
                                        if (booking_period.length > 0) { 
                                            if (vm.sites[index].mooring_class == 'small') {
                                                var total = parseFloat(vm.mooring_book_row_price[index]) + parseFloat(booking_period[0].small_price);
                                                vm.mooring_book_row_price[index] = total.toFixed(2);
                                            } else if (vm.sites[index].mooring_class == 'medium') {
                                                var total = parseFloat(vm.mooring_book_row_price[index]) + parseFloat(booking_period[0].medium_price);
                                                vm.mooring_book_row_price[index] = total.toFixed(2);
                                            } else if (vm.sites[index].mooring_class == 'large') {
                                                var total = parseFloat(vm.mooring_book_row_price[index]) + parseFloat(booking_period[0].large_price);
                                                vm.mooring_book_row_price[index] = total.toFixed(2);
                                            }
                                            if (booking_period.length > 1) {
                                                    vm.mooring_book_row[index] = false;
                                            } else {      
                                                if (booking_period[0].status == 'closed' || booking_period[0].status == 'selected' || booking_period[0].status == 'perday' || booking_period[0].status == 'maxstay' || booking_period[0].status == 'toofar' || booking_period[0].status == 'maxstay') {
                                                    // vm.mooring_book_row[index] = 'disabled';
                                                    vm.mooring_book_row_disabled[index] = true;	
                                                }
                                            }
                                        } else {
                                            vm.mooring_book_row[index] = false;
                                        }
                                    }
                                }
                                var i;
                                for (i = 0; i < filtered_sites.length; i++){
                                    var index;
                                    for (index = 0; index < vm.sites.length; index++){
                                        if (vm.sites[index].id == filtered_sites[i]){
                                            console.log("removed one");
                                            vm.mooring_book_row_display[index] = 'hide';
                                        //    vm.sites.splice(index, 1); 
                                        }
                                    }
                                }

                                console.log("done");

                                // End of booking whole row index
                                vm.status = 'online';
                                if (parseInt(vm.parkstayGroundRatisId) > 0){
                                    vm.parkstayGroundId = data.id;
                                    vm.updateURL();
                                }
	                            if (this.loadID == vm.loadingID) {
                                    vm.isLoading =false;
                                    $('#spinnerLoader').hide();
                                }
                            },
                            error: function(xhr, stat, err) {
                                vm.showSecondErrorLine = true;
                                var max_error = 'Maximum number of people exceeded for the selected campsite';
                                var min_error = 'Number of people is less than the minimum allowed for the selected campsite';
                                if (xhr.responseJSON.hasOwnProperty('closed')){
                                    vm.status = 'closed';
                                }
                                else if (xhr.responseJSON.hasOwnProperty('error') && (xhr.responseJSON.error == max_error || xhr.responseJSON.error == min_error)){
                                    vm.status = 'offline';
                                    vm.showSecondErrorLine = false;
                                }
                                else {
		                      swal.fire({
                		          title: 'Error',
		                          text: 'Uknown Error',
                		          type: 'warning',
                		          showCancelButton: false,
		                          confirmButtonText: 'OK',
	        	                  showLoaderOnConfirm: true,
	       	        	           allowOutsideClick: false
        	                	})

                                    vm.status = 'offline';
                                }
                                if (this.loadID == vm.loadingID) {
                                  vm.isLoading =false;
                                  $('#spinnerLoader').hide();
                                }
                            }
                        });
                    }
                }, 500)();
            }
            
        }
    },
    mounted: function () {
        this.$nextTick(() => {
            var vm = this;

            const rootElement = this.$refs.availabilityWrapper;
            if (rootElement) {
                // Dropdown initializer
                const dropdownElementList = rootElement.querySelectorAll('[data-bs-toggle="dropdown"]');
                [...dropdownElementList].map(dropdownToggleEl => new Dropdown(dropdownToggleEl));

                // Tooltip initializer
                const tooltipTriggerList = rootElement.querySelectorAll('[data-bs-toggle="tooltip"]');
                [...tooltipTriggerList].map(tooltipTriggerEl => new Tooltip(tooltipTriggerEl));
            }

            this.arrivalEl = $('#date-arrival');
            this.update();

                var saneTz = (0 < Math.floor((vm.expiry - moment.now())/1000) < vm.timer);
                var timer = setInterval(function (ev) {
                    // fall back to the pre-encoded timer
                    if (!saneTz) {
                        vm.timer -= 1;
                    } else {
                        // if the timezone is sane, do live updates
                        // this way unloaded tabs won't cache the wrong time.
                        var newTimer = Math.floor((vm.expiry - moment.now())/1000);
                        vm.timer = newTimer;
                    }

                    if ((vm.timer <= -1)) {

                    }
                }, 1000);
            // Fix white space which appears on the right of the availablity screen START
            $('#guests-button').click();
            $('#guests-button').click();
            // Fix white space which appears on the right of the availablity screen END
        })
    }
}
</script>
