/**
 * @file ListsViewTestImpl.java
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
package com.googlecode.alliwant.client.ui;

import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.Widget;
import com.googlecode.alliwant.client.i18n.AiwConstants;
import com.googlecode.alliwant.client.i18n.AiwMessages;

public class ListsViewTestImpl implements ListsView {

  private boolean processing = false;
  private IsWidget header = null;
  
  @Override
  public Widget asWidget() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public void showProcessingOverlay() {
    processing = true;
  }

  @Override
  public void hideProcessingOverlay() {
    processing = false;
  }
  
  public boolean isProcessing() {
    return processing;
  }

  public void setHeader(IsWidget header) {
    this.header = header;
  }
 
  public IsWidget getHeader() {
    return header;
  }

  @Override
  public void clearOwners() {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void addOwnerItem(String item, String value) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void clearLists() {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void addListItem(String item, String value) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setPresenter(Presenter presenter) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public String getOwner() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public String getList() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public void setOwner(String owner) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setList(String list) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setOwnItemsVisible(boolean visible) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setNumOwnItems(int numItems) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setOwnItem(int index, String item) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setOwnItemCategory(int index, String category) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setOwnItemLinkVisible(int index, boolean visible) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setItemsVisible(boolean visible) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setNumItems(int numItems) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setItem(int index, String item) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setItemCategory(int index, String category) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setItemLinkVisible(int index, boolean visible) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setItemStatus(int index, String status) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setItemActionVisible(int index, boolean visible) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void setItemActionText(int index, String text) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public AiwConstants getAiwc() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public void openURL(String url) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public AiwMessages getAiwm() {
    // TODO Auto-generated method stub
    return null;
  }
  
} // ListsViewTestImpl //
