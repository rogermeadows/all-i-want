/**
 * @file JhbViewTestImpl.java
 * @author Adam Meadows
 *
 * Copyright 2011 Adam Meadows 
 *
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS,
 *    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *    See the License for the specific language governing permissions and
 *    limitations under the License.
 *
*/
package com.googlecode.jhb.gwt.client.ui;

import com.google.gwt.user.client.ui.Widget;

public class JhbViewTestImpl implements JhbView {

  private boolean processingOverlayShowing = false;
  
  // ================================================================
  // BEGIN: JhbView methods
  // ================================================================
  
  @Override
  public Widget asWidget() {
    return null;
  }

  @Override
  public void showProcessingOverlay() {
    processingOverlayShowing = true;
  }

  @Override
  public void hideProcessingOverlay() {
    processingOverlayShowing = false;

  }
  
  // ================================================================
  // END: JhbView methods
  // ================================================================
  
  public boolean isProcessingOverlayShowing() {
    return processingOverlayShowing;
  }
  
} // JhbViewTestImpl //